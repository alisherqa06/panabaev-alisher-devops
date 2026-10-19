"""Student information web app using only Python's standard library."""

from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os


STUDENT_FIELDS = (
    ("Name", "STUDENT_NAME", "Alisher"),
    ("Surname", "STUDENT_SURNAME", "Panabaev"),
    ("Group", "STUDENT_GROUP", "It2-2308"),
    ("Student ID", "STUDENT_ID", "37332"),
)


def read_student_info(environment=None):
    """Return student values from an environment mapping, with lab defaults."""
    source = os.environ if environment is None else environment
    return {
        label: source.get(variable) or default
        for label, variable, default in STUDENT_FIELDS
    }


def render_page(info):
    rows = "\n".join(
        "      <tr><th>{}</th><td>{}</td></tr>".format(
            escape(label), escape(value)
        )
        for label, value in info.items()
    )
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>DevOps Student Application</title>
    <style>
      body {{ font: 16px/1.5 system-ui, sans-serif; margin: 3rem auto; max-width: 42rem; padding: 0 1rem; color: #172033; }}
      h1 {{ color: #164e63; }}
      table {{ border-collapse: collapse; width: 100%; }}
      th, td {{ border-bottom: 1px solid #d5dce5; padding: .7rem; text-align: left; }}
      th {{ width: 35%; }}
      .status {{ color: #166534; }}
    </style>
  </head>
  <body>
    <h1>DevOps Student Application</h1>
    <p class="status">Application is running.</p>
    <table aria-label="Student information">
      <tbody>
{rows}
      </tbody>
    </table>
  </body>
</html>
""".format(rows=rows)


def make_handler(info):
    class StudentRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/healthz":
                body = b"ok\n"
                content_type = "text/plain; charset=utf-8"
            elif self.path == "/":
                body = render_page(info).encode("utf-8")
                content_type = "text/html; charset=utf-8"
            else:
                body = b"not found\n"
                content_type = "text/plain; charset=utf-8"
                self.send_response(404)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format, *_args):
            return

    return StudentRequestHandler


def main():
    info = read_student_info()
    print("Student information:", flush=True)
    for label, value in info.items():
        print("{}: {}".format(label, value), flush=True)

    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), make_handler(info))
    print("Listening on 0.0.0.0:{}".format(port), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down.", flush=True)
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
