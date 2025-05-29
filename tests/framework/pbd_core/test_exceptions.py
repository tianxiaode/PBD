import unittest
from pbd_core import PbdException


class TestPbdException(unittest.TestCase):

    def test_happy_path(self):
        message = "Test message"
        code = "1000"
        details = "Test details"
        inner_exception = ValueError("Inner exception")
        log_level = "ERROR"
        exception = PbdException(message, code, details, inner_exception, log_level)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.code, code)
        self.assertEqual(exception.details, details)
        self.assertEqual(str(exception.inner_exception), str(inner_exception))
        self.assertEqual(exception.log_level, log_level)

    def test_no_optional_params(self):
        message = "Test message"
        exception = PbdException(message)
        self.assertEqual(exception.message, message)
        self.assertIsNone(exception.code)
        self.assertIsNone(exception.details)
        self.assertIsNone(exception.inner_exception)
        self.assertIsNone(exception.log_level)

    def test_empty_strings(self):
        message = ""
        code = ""
        details = ""
        log_level = ""
        exception = PbdException(message, code, details, log_level=log_level)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.code, code)
        self.assertEqual(exception.details, details)
        self.assertIsNone(exception.inner_exception)
        self.assertEqual(exception.log_level, log_level)

    def test_none_inner_exception(self):
        message = "Test message"
        exception = PbdException(message, inner_exception=None)
        self.assertEqual(exception.message, message)
        self.assertIsNone(exception.inner_exception)

    def test_inner_exception(self):
        message = "Test message"
        inner_exception = ValueError("Inner exception")
        exception = PbdException(message, inner_exception=inner_exception)
        self.assertEqual(exception.message, message)
        self.assertEqual(str(exception.inner_exception), str(inner_exception))

    def test_log_level(self):
        message = "Test message"
        log_level = "INFO"
        exception = PbdException(message, log_level=log_level)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.log_level, log_level)

    def test_str_method(self):
        message = "Test message"
        code = "1000"
        details = "Test details"
        inner_exception = ValueError("Inner exception")
        log_level = "ERROR"
        exception = PbdException(message, code, details, inner_exception, log_level)
        expected_str = f"PbdException: {{" \
                       f"'message': '{message}', " \
                       f"'code': '{code}', " \
                       f"'details': '{details}', " \
                       f"'inner_exception': '{str(inner_exception)}', " \
                       f"'log_level': '{log_level}'" \
                       f"}}"
        self.assertEqual(str(exception), expected_str)

if __name__ == '__main__':
    unittest.main()