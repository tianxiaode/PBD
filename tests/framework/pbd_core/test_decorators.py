import unittest
from pbd_core import extend_class

class TestExtendClass(unittest.TestCase):
    def test_happy_path(self):
        class MyClass:
            def existing_method(self):
                return "original"

        @extend_class(MyClass)
        class MyExtensions:
            def new_method(self):
                return "new"

            def existing_method(self):
                return self._original_existing_method() + " extended"

        instance = MyClass()
        self.assertEqual(instance.new_method(), "new")
        self.assertEqual(instance.existing_method(), "original extended")

    def test_magic_methods(self):
        class MyClass:
            pass

        @extend_class(MyClass)
        class MyExtensions:
            __magic__ = "custom magic"  # 自定义魔术方法，不应跳过
            __init__ = lambda self: None  # 标准魔术方法，应跳过
            __private = "name mangled"  # 名称修饰属性，应跳过

        print("MyClass __init__ before:", hasattr(MyClass, '__init__'))
        print("MyExtensions __init__:", hasattr(MyExtensions, '__init__'))
        instance = MyClass()
        print("instance __init__ after:", hasattr(instance, '__init__'))        
        # 自定义魔术方法应该被保留
        self.assertEqual(instance.__magic__, "custom magic")
        # 标准魔术方法不应被扩展
        self.assertNotEqual(instance.__init__, MyExtensions.__init__)
        # 名称修饰属性不应被扩展
        self.assertFalse(hasattr(instance, '__private'))        

    def test_edge_case_no_extension_methods(self):
        class MyClass:
            def existing_method(self):
                return "original"

        @extend_class(MyClass)
        class MyExtensions:
            pass

        instance = MyClass()
        self.assertEqual(instance.existing_method(), "original")

    def test_edge_case_extension_with_class_attributes(self):
        class MyClass:
            def existing_method(self):
                return "original"

        @extend_class(MyClass)
        class MyExtensions:
            new_attribute = "attribute"

        instance = MyClass()
        self.assertEqual(instance.existing_method(), "original")
        self.assertEqual(instance.new_attribute, "attribute")

    def test_inheritance_chain(self):
        class BaseClass:
            def method(self):
                return "base"

        class MyClass(BaseClass):
            def method(self):
                return super().method() + " child"

        @extend_class(MyClass)
        class MyExtensions:
            def method(self):
                return self._original_method() + " extended"

        instance = MyClass()
        self.assertEqual(instance.method(), "base child extended")