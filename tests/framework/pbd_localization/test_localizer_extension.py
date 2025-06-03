import unittest
from unittest.mock import Mock, patch
from typing import Optional
from pbd_di import IDependencyBase
from pbd_localization import LocalizerExtension, ILocalizer


class TestLocalizerExtension(unittest.TestCase):
    def setUp(self):
        # 创建一个模拟的IDependencyBase实例
        self.mock_dependency = Mock(spec=IDependencyBase)
        self.mock_dependency._resource_name = "test_resource"
        
        # 设置模拟的get_dependency方法
        self.mock_localizer = Mock(spec=ILocalizer)
        self.mock_dependency.get_dependency = Mock(return_value=self.mock_localizer)
        
        # 应用LocalizerExtension扩展
        # 注意：这里不需要继承，而是直接使用extend_class装饰后的类
        self.test_extension = self.mock_dependency
        #LocalizerExtension._resource_name = "test_resource"
        
        # 确保_localizer初始为None
        if hasattr(self.test_extension, '_localizer'):
            self.test_extension._localizer = None
        else:
            setattr(self.test_extension, '_localizer', None)

    def test_t_method_without_localizer(self):
        # 测试当_localizer为None时，会获取依赖
        test_key = "test_key"
        test_default = "default_value"
        
        # 设置模拟返回值
        self.mock_localizer.get.return_value = "translated_value"
        
        result = LocalizerExtension.t(self.test_extension, test_key, test_default)
        
        # 验证是否正确调用了get_dependency
        self.test_extension.get_dependency.assert_called_once_with(ILocalizer)
        # 验证是否正确调用了localizer的get方法
        self.mock_localizer.get.assert_called_once_with(f"test_resource.{test_key}", test_default)
        # 验证返回值是否正确
        self.assertEqual(result, "translated_value")
        # 验证_localizer是否被缓存
        self.assertEqual(self.test_extension._localizer, self.mock_localizer)

    def test_t_method_with_existing_localizer(self):
        # 测试当_localizer已存在时，直接使用而不重新获取依赖
        test_key = "existing_key"
        self.test_extension._localizer = self.mock_localizer
        
        # 设置模拟返回值
        self.mock_localizer.get.return_value = "cached_translation"
        
        result = LocalizerExtension.t(self.test_extension, test_key)
        
        # 验证没有再次调用get_dependency
        self.test_extension.get_dependency.assert_not_called()
        # 验证是否正确调用了localizer的get方法
        self.mock_localizer.get.assert_called_once_with(f"test_resource.{test_key}", None)
        # 验证返回值是否正确
        self.assertEqual(result, "cached_translation")

    def test_t_method_with_default_value(self):
        # 测试默认值处理
        test_key = "missing_key"
        test_default = "fallback_value"
        
        # 设置模拟返回None，模拟key不存在的情况
        self.mock_localizer.get.return_value = None
        
        result = LocalizerExtension.t(self.test_extension, test_key, test_default)
        
        # 验证是否正确调用了get方法
        self.mock_localizer.get.assert_called_once_with(f"test_resource.{test_key}", test_default)
        # 验证是否正确返回了默认值
        self.assertEqual(result, None)
        
    def test_t_method_without_default_value(self):
        # 测试不提供默认值的情况
        test_key = "another_key"
        
        # 设置模拟返回None
        self.mock_localizer.get.return_value = None
        
        result = LocalizerExtension.t(self.test_extension, test_key)
        
        # 验证是否正确调用了get方法
        self.mock_localizer.get.assert_called_once_with(f"test_resource.{test_key}", None)
        # 验证是否正确返回None
        self.assertIsNone(result)

    def test_t_method_with_missing_resource_name(self):
        # 测试资源名称为空的情况
        self.mock_dependency._resource_name = None
        test_key = "missing_key"
        test_default = "fallback_value"
        
        # 设置模拟返回None
        self.mock_localizer.get.return_value = None
        
        result = LocalizerExtension.t(self.test_extension, test_key, test_default)
        
        # 验证是否正确调用了get方法
        self.mock_localizer.get.assert_called_once_with(f"{test_key}", test_default)
        # 验证是否正确返回了默认值
        self.assertEqual(result, None)



if __name__ == '__main__':
    unittest.main()
