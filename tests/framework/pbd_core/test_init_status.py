from unittest import TestCase
from pbd_core import InitStatusBase

class TestInitStatusBase(TestCase):
    def setUp(self):
        # 每次测试前重置实例状态
        self.init_status_instance = InitStatusBase()
        if hasattr(self.init_status_instance, "_initialized"):
            del self.init_status_instance._initialized

    def test_should_initialize_initial_state(self):
        # 测试初始状态下是否应该初始化
        self.assertTrue(self.init_status_instance.should_initialize())

    def test_mark_initialized_changes_state(self):
        # 测试标记为已初始化后，状态是否正确改变
        self.init_status_instance.mark_initialized()
        self.assertFalse(self.init_status_instance.should_initialize())

    def test_should_initialize_after_marking_initialized(self):
        # 测试标记为已初始化后，再次检查是否应该初始化
        self.init_status_instance.mark_initialized()
        self.assertFalse(self.init_status_instance.should_initialize())

    def test_mark_initialized_twice(self):
        # 测试标记为已初始化两次，状态是否正确
        self.init_status_instance.mark_initialized()
        self.init_status_instance.mark_initialized()
        self.assertFalse(self.init_status_instance.should_initialize())

    def test_initialized_attribute_not_public(self):
        # 测试初始化状态属性是否为非公开属性
        with self.assertRaises(AttributeError):
            self.init_status_instance._initialized
