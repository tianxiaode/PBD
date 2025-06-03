import unittest
from pbd_core import PbdException


class TestPbdException(unittest.TestCase):

    def test_happy_path(self):
        message = "Test message"
        code = "1000"
        details = "Test details"
        inner_exception = ValueError("Inner exception")
        data = {"key": "value"}  # 新增data参数
        exception = PbdException(message, code, details, inner_exception, data)  # 修改构造函数调用
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.code, code)
        self.assertEqual(exception.details, details)
        self.assertEqual(str(exception.inner_exception), str(inner_exception))
        self.assertEqual(exception.data, data)  # 新增对data的断言

    def test_no_optional_params(self):
        message = "Test message"
        exception = PbdException(message)
        self.assertEqual(exception.message, message)
        self.assertIsNone(exception.code)
        self.assertIsNone(exception.details)
        self.assertIsNone(exception.inner_exception)
        self.assertIsNone(exception.data)  # 新增对data的断言

    def test_empty_strings(self):
        message = ""
        code = ""
        details = ""
        data = {}  # 新增空字典
        exception = PbdException(message, code, details, data=data)  # 修改构造函数调用
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.code, code)
        self.assertEqual(exception.details, details)
        self.assertIsNone(exception.inner_exception)
        self.assertEqual(exception.data, data)  # 新增对data的断言

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
        data = {"key": "value"}  # 新增data参数
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

if __name__ == '__main__':
    unittest.main()