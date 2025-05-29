import threading
from unittest import TestCase
from pbd_core import SingletonBase


class TestSingletonBase(TestCase):
    def test_instance_creation(self):
        # 测试实例创建是否为单例
        instance1 = SingletonBase()
        instance2 = SingletonBase()
        self.assertIs(instance1, instance2)

    def test_initialized_state_after_creation(self):
        # 测试实例创建后是否已标记为初始化
        instance = SingletonBase()
        self.assertFalse(instance.should_initialize())

    def test_multiple_instances_in_threads(self):
        # 测试多线程环境下是否仍然为单例
        def create_instance():
            return SingletonBase()

        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        instances = [None] * len(threads)

        for i, thread in enumerate(threads):
            thread.start()

        for i, thread in enumerate(threads):
            thread.join()
            instances[i] = create_instance()

        # 检查所有线程创建的实例是否为同一个
        first_instance = instances[0]
        for instance in instances[1:]:
            self.assertIs(instance, first_instance)


    def test_should_initialize_after_creation(self):
        # 测试在实例创建之后是否应该初始化
        instance = SingletonBase()
        self.assertFalse(instance.should_initialize())

    def test_mark_initialized_manually(self):
        # 测试手动标记为已初始化
        instance = SingletonBase()
        if hasattr(instance, "_initialized"):
            del instance._initialized
        instance.mark_initialized()
        self.assertFalse(instance.should_initialize())


    def test_instances_dict(self):
        # 测试单例实例字典是否正确存储实例
        instance = SingletonBase()
        self.assertIn(SingletonBase, SingletonBase._instances)
        self.assertIs(instance, SingletonBase._instances[SingletonBase])


    def test_new_method_called_once(self):
        # 测试 __new__ 方法是否只被调用一次
        instance = SingletonBase()
        with self.assertRaises(AttributeError):
            # 尝试访问私有属性 _new_called
            _ = instance._new_called

        # 使用一个子类来验证 __new__ 是否只被调用一次
        class TestSingleton(SingletonBase):
            def __new__(cls, *args, **kwargs):
                if not hasattr(cls, "_new_called"):
                    cls._new_called = True
                return super().__new__(cls)

        test_instance = TestSingleton()
        self.assertTrue(hasattr(TestSingleton, "_new_called"))
        self.assertIs(test_instance, TestSingleton._instances[TestSingleton])
