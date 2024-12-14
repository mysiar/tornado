import io
import logging
import sys
import unittest
from unittest import mock

from tornado.simple_httpclient import HTTPStreamClosedError
from tornado.test.httpserver_test import EchoHandler
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application


class DefaultSettingsHTTPTestCase(AsyncHTTPTestCase):
    """
    setUp & tearDown only to supress log as it cause test failure in GitHub ci
    """

    def setUp(self):
        super().setUp()
        self.saved_stderr = sys.stderr
        self.saved_logger_level = logging.getLogger("tornado").level

    def tearDown(self):
        sys.stderr = self.saved_stderr
        logging.getLogger("tornado").setLevel(self.saved_logger_level)
        super().tearDown()

    def get_app(self):
        return Application(
            [
                ("/echo", EchoHandler),
            ]
        )

    def test_query_string_long_failing(self):
        long = "abcde" * 14000

        with mock.patch("sys.stderr", new_callable=io.StringIO):
            logging.getLogger("tornado").setLevel(logging.CRITICAL)
            with self.assertRaises(HTTPStreamClosedError):
                self.fetch(f"/echo?foo={long}")
            logging.getLogger("tornado").setLevel(self.saved_logger_level)
            sys.stderr = self.saved_stderr


if __name__ == "__main__":
    unittest.main()
