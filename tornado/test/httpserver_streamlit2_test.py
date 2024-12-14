import unittest

from tornado.escape import json_decode
from tornado.test.httpserver_test import EchoHandler
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application


class CustomSettingsHTTPTestCase(AsyncHTTPTestCase):
    def get_httpserver_options(self):
        return {
            "max_header_size": 2 * 1024 * 1024,
        }

    def get_app(self):
        return Application(
            [
                ("/echo", EchoHandler),
            ]
        )

    def test_query_string_long_failing(self):
        long = "abcde" * 400000
        response = self.fetch(f"/echo?foo={long}")
        data = json_decode(response.body)
        self.assertDictEqual({"foo": [f"{long}"]}, data)


if __name__ == "__main__":
    unittest.main()
