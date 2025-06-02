import unittest
from pbd_core import StringHelper

class TestStringHelper(unittest.TestCase):
    """StringHelper 单元测试"""
    
    def test_camel_to_snake(self):
        """测试驼峰转蛇形命名"""
        test_cases = [
            ("", ""),  # 空字符串
            ("simple", "simple"),  # 无转换
            ("CamelCase", "camel_case"),  # 基本转换
            ("HTTPRequest", "http_request"),  # 连续大写
            ("user2API", "user2_api"),  # 包含数字
            ("_PrivateVar", "_private_var"),  # 保留前缀下划线
             ("__Internal", "_internal"),     # 多个下划线
            ("mixed_CaseTest", "mixed_case_test"),  # 混合下划线
            ("ABC", "abc"),  # 全大写
            ("already_snake", "already_snake"),  # 已经是蛇形
            ("Number123InMiddle", "number123_in_middle"),  # 中间数字
            ("_XMLParser", "_xml_parser"),   # 下划线加大写
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                self.assertEqual(StringHelper.camel_to_snake(input_str), expected)
    
    def test_safe_truncate_utf8(self):
        """测试UTF-8安全截断"""
        # 测试ASCII字符
        self.assertEqual(StringHelper.safe_truncate_utf8("hello", 3), "hel")
        self.assertEqual(StringHelper.safe_truncate_utf8("hello", 5), "hello")
        
        # 测试中文(每个中文字符占3字节)
        chinese = "你好世界"
        self.assertEqual(StringHelper.safe_truncate_utf8(chinese, 6), "你好")  # 6字节=2中文字
        self.assertEqual(StringHelper.safe_truncate_utf8(chinese, 5), "你")  # 5字节截断1中文字
        
        # 测试混合字符
        mixed = "hello你好"
        self.assertEqual(StringHelper.safe_truncate_utf8(mixed, 8), "hello你")  # h(1)*5 + 你(3)
        
        # 测试空字符串
        self.assertEqual(StringHelper.safe_truncate_utf8("", 10), "")
        
        # 测试None
        self.assertEqual(StringHelper.safe_truncate_utf8(None, 10), None)
        
        # 测试边界条件
        self.assertEqual(StringHelper.safe_truncate_utf8("a", 0), "")
        
        # 测试不完整字符截断
        emoji = "😀"  # 4字节
        self.assertEqual(StringHelper.safe_truncate_utf8(emoji, 3), "")  # 不完整字符被忽略
    
    def test_is_empty(self):
        """测试字符串空判断"""
        self.assertTrue(StringHelper.is_empty(""))
        self.assertTrue(StringHelper.is_empty(None))
        self.assertFalse(StringHelper.is_empty(" "))
        self.assertFalse(StringHelper.is_empty("hello"))
        self.assertFalse(StringHelper.is_empty("0"))

if __name__ == '__main__':
    unittest.main()
