#!/usr/bin/env python3
"""Wait for the student app and verify its health and rendered data."""

import os
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen


DEFAULTS = {
    "STUDENT_NAME": "Alisher",
    "STUDENT_SURNAME": "Panabaev",
    "STUDENT_GROUP": "It2-2308",
    "STUDENT_ID": "37332",
}


def expected_values():
    return {key: os.environ.get(key) or value for key, value in DEFAULTS.items()}


def verify(base_url):
    deadline = time.monotonic() + 30
    last_error = None
    while time.monotonic() < deadline:
        try:
            with urlopen(base_url.rstrip("/") + "/healthz", timeout=2) as response:
                if response.status != 200 or response.read() != b"ok\n":
                    raise RuntimeError("health endpoint returned an unexpected response")
            with urlopen(base_url.rstrip("/") + "/", timeout=2) as response:
                page = response.read().decode("utf-8")
                if response.status != 200:
                    raise RuntimeError("student page returned HTTP {}".format(response.status))
            missing = [value for value in expected_values().values() if value not in page]
            if missing:
                raise RuntimeError("student page is missing expected values: {}".format(missing))
            print("HTTP smoke check passed at {}".format(base_url))
            for key, value in expected_values().items():
                print("{}={}".format(key, value))
            return
        except (URLError, OSError, RuntimeError) as error:
            last_error = error
            time.sleep(1)
    raise SystemExit("HTTP smoke check failed after 30 seconds: {}".format(last_error))


if __name__ == "__main__":
    verify(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080")
