import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen

from app.server import make_handler, read_student_info, render_page


class StudentInfoTests(unittest.TestCase):
    def test_defaults_are_personalized(self):
        self.assertEqual(
            read_student_info({}),
            {
                "Name": "Alisher",
                "Surname": "Panabaev",
                "Group": "It2-2308",
                "Student ID": "37332",
            },
        )

    def test_environment_values_override_defaults(self):
        info = read_student_info(
            {
                "STUDENT_NAME": "Test Name",
                "STUDENT_SURNAME": "Test Surname",
                "STUDENT_GROUP": "Test Group",
                "STUDENT_ID": "12345",
            }
        )
        self.assertEqual(info["Name"], "Test Name")
        self.assertEqual(info["Surname"], "Test Surname")
        self.assertEqual(info["Group"], "Test Group")
        self.assertEqual(info["Student ID"], "12345")

    def test_html_escapes_student_values(self):
        page = render_page({"Name": "<script>alert(1)</script>"})
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertNotIn("<script>alert(1)</script>", page)

    def test_health_and_student_pages(self):
        info = read_student_info({})
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(info))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base_url = "http://127.0.0.1:{}".format(server.server_port)
        try:
            with urlopen(base_url + "/healthz", timeout=3) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.read(), b"ok\n")
            with urlopen(base_url + "/", timeout=3) as response:
                page = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertIn("Alisher", page)
                self.assertIn("Panabaev", page)
                self.assertIn("It2-2308", page)
                self.assertIn("37332", page)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
