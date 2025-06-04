import unittest
from pbd_core.exceptions import PbdException, InternalException, BusinessException, SimpleMessageException


class TestPbdException(unittest.TestCase):

    def test_happy_path(self):
        message = "Test message"
        code = "1000"
        details = "Test details"
        inner_exception = ValueError("Inner exception")
        data = {"key": "value"}
        exception = PbdException(message, code, details, inner_exception, data)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.code, code)
        self.assertEqual(exception.details, details)
        self.assertEqual(str(exception.inner_exception), str(inner_exception))
        self.assertEqual(exception.data, data)

    def test_no_optional_params(self):
        message = "Test message"
        exception = PbdException(message)
        self.assertEqual(exception.message, message)
        self.assertIsNone(exception.code)
        self.assertIsNone(exception.details)
        self.assertIsNone(exception.inner_exception)
        self.assertIsNone(exception.data)

    def test_empty_strings(self):
        message = ""
        code = ""
        details = ""
        data = {}
        exception = PbdException(message, code, details, data=data)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.code, code)
        self.assertEqual(exception.details, details)
        self.assertIsNone(exception.inner_exception)
        self.assertEqual(exception.data, data)

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

    def test_str_method(self):
        message = "Test message"
        code = "1000"
        details = "Test details"
        inner_exception = ValueError("Inner exception")
        data = {"key": "value"}
        exception = PbdException(message, code, details, inner_exception, data)
        expected_str = f"PbdException: {{" \
                    f"'message': '{message}', " \
                    f"'code': '{code}', " \
                    f"'details': '{details}', " \
                    f"'inner_exception': '{str(inner_exception)}', " \
                    f"'data': {data}" \
                    f"}}"
        self.assertEqual(str(exception), expected_str)

    def test_data_parameter(self):
        message = "Test message"
        data = {"key1": "value1", "key2": 123}
        exception = PbdException(message, data=data)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.data, data)
        self.assertIsNone(exception.code)
        self.assertIsNone(exception.details)
        self.assertIsNone(exception.inner_exception)


class TestInternalException(unittest.TestCase):
    def test_internal_exception(self):
        message = "Internal error"
        exception = InternalException(message)
        self.assertEqual(exception.message, message)
        self.assertFalse(exception.expose)
        
    def test_internal_exception_with_all_params(self):
        message = "Internal error"
        code = "500"
        details = "Detailed error info"
        inner_exception = ValueError("Value error")
        data = {"trace": "stack"}
        exception = InternalException(message, code, details, inner_exception, data)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.code, code)
        self.assertEqual(exception.details, details)
        self.assertEqual(str(exception.inner_exception), str(inner_exception))
        self.assertEqual(exception.data, data)
        self.assertFalse(exception.expose)


class TestBusinessException(unittest.TestCase):
    def test_business_exception(self):
        message = "Business error"
        exception = BusinessException(message)
        self.assertEqual(exception.message, message)
        self.assertTrue(exception.expose)
        
    def test_business_exception_with_all_params(self):
        message = "Business error"
        code = "400"
        details = "Invalid input"
        inner_exception = TypeError("Type error")
        data = {"field": "name"}
        exception = BusinessException(message, code, details, inner_exception, data)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.code, code)
        self.assertEqual(exception.details, details)
        self.assertEqual(str(exception.inner_exception), str(inner_exception))
        self.assertEqual(exception.data, data)
        self.assertTrue(exception.expose)


class TestSimpleMessageException(unittest.TestCase):
    def test_simple_message_exception(self):
        message = "Simple error message"
        exception = SimpleMessageException(message)
        self.assertEqual(exception.message, message)
        self.assertTrue(exception.expose)
        self.assertIsNone(exception.code)
        self.assertIsNone(exception.details)
        self.assertIsNone(exception.inner_exception)
        self.assertIsNone(exception.data)


if __name__ == '__main__':
    unittest.main()
