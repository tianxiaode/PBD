import unittest
from unittest.mock import MagicMock
from pbd_di import IDependencyBase, ISingletonDependency, ITransientDependency, IScopedDependency,IReplaceableInterface, IServiceProvider

class TestIReplaceableInterface(unittest.TestCase):
    def test_is_interface_direct_inheritance(self):
        class BaseInterface(IReplaceableInterface):
            pass

        self.assertTrue(BaseInterface.is_interface())

    def test_is_interface_not_direct_inheritance(self):
        class BaseInterface(IReplaceableInterface):
            pass

        class DerivedInterface(BaseInterface):
            pass

        self.assertFalse(DerivedInterface.is_interface())

    def test_registers_implementation_in_non_interface(self):
        class BaseInterface(IReplaceableInterface):
            pass

        class DerivedClass(BaseInterface):
            pass

        self.assertTrue(hasattr(BaseInterface, '__di_implementation__'))
        self.assertEqual(BaseInterface.__di_implementation__, DerivedClass)

    def test_registers_implementation_deep_in_hierarchy(self):
        class IRepository:
            pass

        class IUserRepository(IRepository, IReplaceableInterface):
            pass    

        class UserRepository(IUserRepository):
            pass
        
        self.assertFalse(hasattr(IReplaceableInterface, '__di_implementation__'))
        self.assertFalse(hasattr(IRepository, '__di_implementation__'))
        self.assertTrue(hasattr(IUserRepository, '__di_implementation__'))
        self.assertEqual(IUserRepository.__di_implementation__, UserRepository)



class TestIServiceProvider(unittest.TestCase):
    def test_get_service_abstractmethod(self):
        with self.assertRaises(TypeError):
            class Derived(IServiceProvider):
                pass

            Derived()

        

class TestDependencyBase(unittest.TestCase):
    def test_init_subclass_inherits_dependencies(self):

        class BaseDependency:
            pass
        
        class Base(IDependencyBase):
            _deps = [BaseDependency]

        class Derived(Base):
            pass

        self.assertTrue(any(dep is BaseDependency for dep in Derived.deps.values()))

    def test_init_subclass_adds_current_dependencies(self):
        # 使用 type 动态创建类并明确指定模块路径
        NewDependency = type(
            'NewDependency', 
            (), 
            {'__module__': 'pbd_di.test_dependencybase'}
        )
        
        class Base(IDependencyBase):
            pass        
        
        class Derived(Base):
            _deps = [NewDependency]
        
        # 修正预期的键名
        expected_key = 'pbd_di.test_dependencybase.newdependency'
        self.assertIn(expected_key, Derived.deps)
        self.assertIsInstance(Derived.deps[expected_key], type)


    def test_init_subclass_removes__deps_after_assignment(self):
        class NewDependency:
            pass

        class Base(IDependencyBase):
            pass

        class Derived(Base):
            _deps = [NewDependency]

        self.assertFalse(hasattr(Derived, '_deps'))

    def test_get_default_dependency_name(self):
        # 在模块层级定义测试类，避免嵌套在方法中
        class NewDependency:
            pass
        
        # 临时修改类的 __module__ 和 __qualname__ 以模拟正常情况
        NewDependency.__module__ = 'pbd_di.test_dependencybase'
        NewDependency.__qualname__ = 'NewDependency'
        
        name = IDependencyBase._get_default_dependency_name(NewDependency)
        self.assertEqual(name, 'pbd_di.test_dependencybase.newdependency')

    def test_init_sets_dependencies_from_kwargs(self):
        # 准备测试依赖
        mock_dep1 = MagicMock()
        mock_dep2 = MagicMock()
        
        # 创建测试实例并注入依赖
        class TestClass(IDependencyBase):
            pass
        
        instance = TestClass(dep1=mock_dep1, dep2=mock_dep2)
        
        # 验证依赖是否正确注入
        self.assertEqual(instance.dep1, mock_dep1)
        self.assertEqual(instance.dep2, mock_dep2)       

    def test_get_dependency_returns_correct_dependency(self):
        # 创建测试类
        TestDependency = type(
            'TestDependency', 
            (), 
            {'__module__': 'pbd_di.test_dependencybase'}
        )
        
        class TestClass(IDependencyBase):
            _deps = [TestDependency]
        
        # 测试获取依赖
        ctor_args = {}
        for name, dep in TestClass.deps.items():
            ctor_args[name] = dep()
        instance = TestClass(**ctor_args)
        result = instance.get_dependency(TestDependency)
        self.assertTrue(isinstance(result, TestDependency))  

    def test_get_dependency_raises_error_if_not_found(self):
        TestDependency = type(
            'TestDependency', 
            (), 
            {'__module__': 'pbd_di.test_dependencybase'}
        )

        # 创建测试类
        class TestClass(IDependencyBase):
            pass
        
        # 测试获取不存在的依赖
        with self.assertRaises(ValueError):
            instance = TestClass()
            instance.get_dependency(TestDependency)      

class TestSingletonDependency(unittest.TestCase):
    def test_init_subclass_sets_scope_to_singleton(self):
        class Derived(ISingletonDependency):
            pass

        self.assertEqual(Derived._di_scope, 'singleton')

class TestTransientDependency(unittest.TestCase):
    def test_init_subclass_sets_scope_to_transient(self):
        class Derived(ITransientDependency):
            pass

        self.assertEqual(Derived._di_scope, 'transient')

class TestScopedDependency(unittest.TestCase):
    def test_init_subclass_sets_scope_to_scoped(self):
        class Derived(IScopedDependency):
            pass

        self.assertEqual(Derived._di_scope, 'scoped')