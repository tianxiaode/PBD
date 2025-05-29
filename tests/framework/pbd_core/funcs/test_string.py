import unittest 
from pbd_core import camel_to_snake, safe_truncate_utf8, is_empty

class TestStringFunctions(unittest.TestCase):
    def test_camel_to_snake_happy_path(self):
        self.assertEqual(camel_to_snake("CamelCaseString"), "camel_case_string")
        self.assertEqual(camel_to_snake("HTTPRequest"), "http_request")
        self.assertEqual(camel_to_snake("user2API"), "user2_api")
        self.assertEqual(camel_to_snake("XMLHttpRequest"), "xml_http_request")
        self.assertEqual(camel_to_snake("convertToSnakeCase"), "convert_to_snake_case")

    def test_camel_to_snake_edge_cases(self):
        self.assertEqual(camel_to_snake(""), "")
        self.assertEqual(camel_to_snake("Already_snake_case"), "already_snake_case")
        self.assertEqual(camel_to_snake("JSON"), "json")
        self.assertEqual(camel_to_snake("One"), "one")
        self.assertEqual(camel_to_snake("A"), "a")

    def test_safe_truncate_utf8_happy_path(self):
        self.assertEqual(safe_truncate_utf8("Hello, World!", 12), "Hello, World")
        self.assertEqual(safe_truncate_utf8("你好，世界！", 12), "你好，世")
        self.assertEqual(safe_truncate_utf8("Mixed 英文和中文", 15), "Mixed 英文和")

    def test_safe_truncate_utf8_edge_cases(self):
        self.assertEqual(safe_truncate_utf8("", 10), "")
        self.assertEqual(safe_truncate_utf8("Short", 10), "Short")
        self.assertEqual(safe_truncate_utf8("你好，世界！", 1), "")
        self.assertEqual(safe_truncate_utf8("你好，世界！", 0), "")
        self.assertEqual(safe_truncate_utf8("Unicode \u1234", 8), "Unicode")

    def test_is_empty_happy_path(self):
        self.assertTrue(is_empty(None))
        self.assertTrue(is_empty(""))
        self.assertFalse(is_empty("Not empty"))
        self.assertFalse(is_empty(" "))
        self.assertFalse(is_empty("0"))

    def test_is_empty_edge_cases(self):
        self.assertTrue(is_empty(""))
        self.assertFalse(is_empty("a"))
        self.assertFalse(is_empty("123"))
        self.assertFalse(is_empty("False"))
        self.assertFalse(is_empty("None"))

if __name__ == '__main__':
    unittest.main()
