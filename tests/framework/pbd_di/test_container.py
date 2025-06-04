import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from pbd_di import (
    Container, SINGLETON, TRANSIENT,scoped_context, ISingletonDependency, IScopedDependency, ITransientDependency,
    CircularDependencyException, InvalidScopeException, get_default_dependency_name
)


class ContainerTestCase(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        Container._instance = None
        self.container = Container()
        self.MockScopedService = type('MockScopedService', (IScopedDependency,), {})
        self.MockTransientService = type('MockTransientService', (ITransientDependency,), {})
        self.MockSingletonService = type('MockSingletonService', (ISingletonDependency,), {})

    async def test_get_singleton(self):
        MockSingletonService = self.MockSingletonService
        service = MockSingletonService()
        container = self.container
        with patch.object(container, '_create_instance', AsyncMock(return_value=service)):
            instance = await container.get(MockSingletonService)
            self.assertEqual(await container.get(MockSingletonService), instance)
            container._create_instance.assert_called_once()

    async def test_get_scoped(self):
        container = self.container
        MockScopedService = self.MockScopedService
        service1 = MockScopedService()
        service2 = MockScopedService()  # 创建第二个不同的mock对象
        
        # 使用side_effect而不是return_value
        with patch.object(container, '_create_instance', AsyncMock(side_effect=[service1, service2])):
            async with container._scoped_context.scope():
                instance1 = await container.get(MockScopedService)
                instance2 = await container.get(MockScopedService)
                self.assertEqual(instance1, instance2)  # 同一作用域内相同
                container._create_instance.assert_called_once()  # 只创建一次
                
            async with container._scoped_context.scope():
                instance3 = await container.get(MockScopedService)
                self.assertNotEqual(instance1, instance3)  # 不同作用域应该不同
                self.assertEqual(container._create_instance.call_count, 2)  # 应该创建了两次
    
    async def test_invalid_scope(self):
        container = self.container
        with self.assertRaises(InvalidScopeException) as context:
            class InvalidService:
                _di_scope = 'invalid'
                deps = {}
            await container.get(InvalidService)
        self.assertEqual(context.exception.code, "Invalid scope exception")
        self.assertEqual(context.exception.data, {"target": "InvalidService", "scope": "invalid"})
        self.assertEqual(str(context.exception.message), "无法解析 InvalidService 的作用域 invalid")

    async def test_get_transient(self):
        container = self.container
        # 创建两个不同的 mock 对象
        MockTransientService = self.MockTransientService
        service1 = MockTransientService()
        service2 = MockTransientService()
        
        # 使用 side_effect 而不是 return_value
        with patch.object(container, '_create_instance', AsyncMock(side_effect=[service1, service2])):
            instance1 = await container.get(MockTransientService)
            instance2 = await container.get(MockTransientService)
            self.assertNotEqual(instance1, instance2)  # 现在应该不同了
            self.assertEqual(container._create_instance.call_count, 2)  # 确保调用了两次

    async def test_initialize(self):
        container = self.container
        MockTransientService = self.MockTransientService
        MockTransientService.initialize = AsyncMock()
        instance = await container.get(MockTransientService)
        instance.initialize.assert_awaited_once()

        MockTransientService.initialize = MagicMock()
        instance = await container.get(MockTransientService)
        instance.initialize.assert_called_once()

    async def test_get_implementation(self):
        container = self.container
        MockService = self.MockTransientService
        service = type(
            'MockServiceImplementation', 
            (MockService,), 
            {'__module__': 'pbd_di.test_container'}
        )
        service2 = MockService()
        service2.__di_implementation__ = service
        with patch.object(container, '_create_instance', AsyncMock(return_value=service)):
            instance = await container.get(service2)
            self.assertEqual(instance, service)
            container._create_instance.assert_called_once()

    async def test_get_circular_dependency(self):
        CircularService1 = type(
            'CircularService1', 
            (), 
            {'__module__': 'pbd_di.test_container', "_di_scope": SINGLETON}
        )

        class CircularService2:
            _di_scope = SINGLETON
            deps = {}

        # 定义完成后设置依赖
        CircularService1.deps = {'circular_service2': CircularService2}
        CircularService2.deps = {'circular_service1': CircularService1}
        container = self.container
        with self.assertRaises(CircularDependencyException) as context:
            await container.get(CircularService1)
        self.assertEqual(context.exception.code, "Circular dependency exception")
        self.assertEqual(context.exception.data, {"name": "pbd_di.test_container.CircularService1"})
        self.assertEqual(str(context.exception.message), "检查到循环依赖： pbd_di.test_container.CircularService1")

    async def test_shutdown(self):
        container = self.container
        MockSingletonService1 = type('MockSingletonService1', (ISingletonDependency,), { "close":AsyncMock() })
        MockSingletonService2 = type('MockSingletonService2', (ISingletonDependency,), { "close":MagicMock() })
        MockScopedService = self.MockScopedService
        MockScopedService.close = AsyncMock()
        service1 = await container.get(MockSingletonService1)
        service2 = await container.get(MockSingletonService2)
        async with container._scoped_context.scope():
            scope_service =await container.get(MockScopedService)
        await container.shutdown()

        service1.close.assert_awaited_once()
        service2.close.assert_called_once()
        scope_service.close.assert_awaited_once()

    async def test_get_with_context_instances(self):
        container = self.container

        MockService1 = type('MockService1', (ITransientDependency,),{'__module__': 'pbd_di.test_container'})
        MockService2 = type('MockService2', (ITransientDependency,),{})
        
        # 创建主服务类，它有2个依赖
        class MainService(ITransientDependency):
            _deps = [MockService2]
            
        
        service1 = MockService1()
        
        # 使用patch模拟Dep2Service的创建
        original_create_instance = container._create_instance

        call_count = 0  # 用于追踪调用次数

        context_instances  = {}
        context_instances[get_default_dependency_name(MockService1)] = service1

        async def custom_side_effect(cls, *args, **kwargs):
            nonlocal call_count
            return await original_create_instance(cls, *args, **kwargs)

        with patch.object(container, '_create_instance', new=AsyncMock(side_effect=custom_side_effect)) as mock_create:
            # 调用get方法并传入context_instances
            instance = await container.get(
                MainService,
                context_instances=context_instances
            )
            
            self.assertEqual(mock_create.call_count, 2) 
            
            # 验证实例创建正确
            self.assertIsInstance(instance, MainService)
            self.assertIs(instance.get_dependency(MockService1), service1)  # 来自context_instances
            self.assertIsInstance(instance.get_dependency(MockService2), MockService2)  # 来自容器解析
            

