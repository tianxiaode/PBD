import threading
from unittest import TestCase
from pbd_core import SingletonBase

class TestSingleton(TestCase):
    class TestImpl(SingletonBase):
        def initialize(self):
            self.value = 42
            self.initialized = True

    def test_singleton_behavior(self):
        """测试单例基础特性"""
        instance1 = self.TestImpl()
        instance2 = self.TestImpl()
        self.assertIs(instance1, instance2)
        self.assertEqual(instance1.value, 42)

    def test_initialize_once(self):
        """测试初始化只执行一次"""
        instance = self.TestImpl()
        init_count = 0
        
        class CounterImpl(SingletonBase):
            def initialize(self):
                nonlocal init_count
                init_count += 1
                self.count = init_count
        
        obj1 = CounterImpl()
        obj2 = CounterImpl()
        self.assertEqual(obj1.count, 1)
        self.assertEqual(obj2.count, 1)

    def test_thread_safety(self):
        """测试线程安全"""
        results = []
        
        def create_instance():
            instance = self.TestImpl()
            results.append(instance.value)
        
        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            
        self.assertTrue(all(x == 42 for x in results))
        self.assertEqual(len(set(results)), 1)

    def test_init_override_protection(self):
        """测试禁止重写__init__的保护"""
        with self.assertRaises(TypeError):
            class BadSingleton(SingletonBase):
                def __init__(self):
                    pass

    def test_multiple_subclasses(self):
        """测试多个子类互不干扰"""
        class A(SingletonBase):
            def initialize(self):
                self.type = 'A'
                
        class B(SingletonBase):
            def initialize(self):
                self.type = 'B'
                
        a1, a2 = A(), A()
        b1, b2 = B(), B()
        
        self.assertIs(a1, a2)
        self.assertIs(b1, b2)
        self.assertIsNot(a1, b1)
        self.assertEqual(a1.type, 'A')
        self.assertEqual(b1.type, 'B')

