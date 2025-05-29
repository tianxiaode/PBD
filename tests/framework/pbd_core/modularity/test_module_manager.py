import unittest
from unittest import mock,IsolatedAsyncioTestCase
from unittest.mock import Mock, patch
from pbd_core import ModuleManager, ModuleLoadError

class TestModuleManager(IsolatedAsyncioTestCase):
    def setUp(self):
        self.root_module = Mock()
        self.root_module.__name__ = 'RootModule'
        self.mod_a = Mock()
        self.mod_a.__name__ = 'ModuleA'
        self.mod_b = Mock()
        self.mod_b.__name__ = 'ModuleB'
        self.mod_c = Mock()
        self.mod_c.__name__ = 'ModuleC'

        self.root_module._deps = [self.mod_a]
        self.mod_a._deps = [self.mod_b]
        self.mod_b._deps = [self.mod_c]
        self.mod_c._deps = []

        self.manager = ModuleManager(self.root_module)

    def test_topo_sort_happy_path(self):
        with patch('pbd_core.ModuleManager.logger') as mock_logger:
            self.manager._topo_sort(self.root_module)
            self.assertEqual(self.manager._init_order, [self.mod_c, self.mod_b, self.mod_a, self.root_module])
            mock_logger.debug.assert_any_call("开始处理模块 RootModule")
            mock_logger.debug.assert_any_call("模块 RootModule 依赖 ModuleA")
            mock_logger.debug.assert_any_call("开始处理模块 ModuleA")
            mock_logger.debug.assert_any_call("模块 ModuleA 依赖 ModuleB")
            mock_logger.debug.assert_any_call("开始处理模块 ModuleB")
            mock_logger.debug.assert_any_call("模块 ModuleB 依赖 ModuleC")
            mock_logger.debug.assert_any_call("开始处理模块 ModuleC")
            mock_logger.info.assert_any_call("模块 ModuleC 添加到初始化顺序")
            mock_logger.info.assert_any_call("模块 ModuleB 添加到初始化顺序")
            mock_logger.info.assert_any_call("模块 ModuleA 添加到初始化顺序")
            mock_logger.info.assert_any_call("模块 RootModule 添加到初始化顺序")

    def test_topo_sort_module_visited(self):
        self.manager._visited.add(self.mod_a)
        with patch('pbd_core.ModuleManager.logger') as mock_logger:
            self.manager._topo_sort(self.mod_a)
            mock_logger.debug.assert_any_call("模块 ModuleA 已经访问过，跳过")

    def test_topo_sort_cycle_dependency(self):
        self.mod_c._deps = [self.root_module]
        with patch('pbd_core.ModuleManager.logger') as mock_logger:
            with self.assertRaises(ModuleLoadError) as context:
                self.manager._topo_sort(self.root_module)
            
            # 验证错误消息包含循环依赖路径（不严格检查顺序）
            error_msg = str(context.exception)
            self.assertTrue(
                "循环依赖检测到模块链路:" in error_msg and
                all(m in error_msg for m in ["RootModule", "ModuleA", "ModuleB", "ModuleC"]),
                f"错误消息格式不正确: {error_msg}"
            )
            
            # 验证日志调用
            mock_logger.error.assert_any_call(
                mock.ANY  # 不严格检查日志中的路径顺序
            )

    def test_topo_sort_no_dependencies(self):
        with patch('pbd_core.ModuleManager.logger') as mock_logger:
            self.manager._topo_sort(self.mod_c)
            self.assertIn(self.mod_c, self.manager._init_order)
            mock_logger.debug.assert_any_call("开始处理模块 ModuleC")
            mock_logger.info.assert_any_call("模块 ModuleC 添加到初始化顺序")

    def test_collect_and_sort(self):
        # 测试正常依赖关系
        with patch('pbd_core.ModuleManager.logger') as mock_logger:
            result = self.manager.collect_and_sort()
            
            # 验证返回的顺序是否正确
            self.assertEqual(result, [self.mod_c, self.mod_b, self.mod_a, self.root_module])
            
            # 验证日志调用
            mock_logger.info.assert_any_call(f"开始收集模块依赖并拓扑排序，根模块: RootModule")
            mock_logger.info.assert_any_call("模块拓扑排序完成，初始化顺序如下:")
            mock_logger.info.assert_any_call(" - ModuleC")
            mock_logger.info.assert_any_call(" - ModuleB")
            mock_logger.info.assert_any_call(" - ModuleA")
            mock_logger.info.assert_any_call(" - RootModule")

    def test_collect_and_sort_with_cycle_dependency(self):
        # 测试循环依赖情况
        self.mod_c._deps = [self.root_module]  # 创建循环依赖
        with patch('pbd_core.ModuleManager.logger') as mock_logger:
            with self.assertRaises(ModuleLoadError):
                self.manager.collect_and_sort()
            
            # 验证日志调用
            mock_logger.info.assert_called_with(f"开始收集模块依赖并拓扑排序，根模块: RootModule")
            mock_logger.error.assert_called()

    async def test_initialize_modules_happy_path(self):
        # 准备模拟模块类
        for mod in [self.root_module, self.mod_a, self.mod_b, self.mod_c]:
            mod.return_value = Mock()  # 模拟模块实例
            mod.return_value.pre_configure = Mock()
            mod.return_value.configure = Mock()
            mod.return_value.post_configure = Mock()

        with patch('pbd_core.ModuleManager.logger') as mock_logger:
            instances = await self.manager.initialize_modules()
            
            # 验证返回的实例字典
            self.assertEqual(len(instances), 4)
            self.assertIsInstance(instances[self.root_module], Mock)
            self.assertIsInstance(instances[self.mod_a], Mock)
            self.assertIsInstance(instances[self.mod_b], Mock)
            self.assertIsInstance(instances[self.mod_c], Mock)
            
            # 验证初始化方法调用顺序
            for mod in [self.mod_c, self.mod_b, self.mod_a, self.root_module]:
                instances[mod].pre_configure.assert_called_once()
                instances[mod].configure.assert_called_once()
                instances[mod].post_configure.assert_called_once()
            
            # 验证日志调用
            mock_logger.info.assert_any_call("开始初始化模块")
            mock_logger.info.assert_any_call("实例化模块 RootModule")
            mock_logger.info.assert_any_call("开始执行阶段: pre_configure")
            mock_logger.info.assert_any_call("开始执行阶段: configure")
            mock_logger.info.assert_any_call("开始执行阶段: post_configure")
            mock_logger.info.assert_any_call("所有模块初始化完成")

    async def test_initialize_modules_with_missing_methods(self):
        # 准备模拟模块类，部分模块缺少某些方法
        for mod in [self.root_module, self.mod_a, self.mod_b, self.mod_c]:
            mod.return_value = Mock()
        
        # 移除某些模块的方法
        del self.mod_a.return_value.configure
        del self.mod_b.return_value.post_configure

        with patch('pbd_core.ModuleManager.logger') as mock_logger:
            instances = await self.manager.initialize_modules()
            
            # 验证仍然成功初始化
            self.assertEqual(len(instances), 4)
            
            # 验证缺少的方法没有被调用
            self.mod_a.return_value.pre_configure.assert_called_once()
            self.assertFalse(hasattr(self.mod_a.return_value, 'configure'))
            self.mod_a.return_value.post_configure.assert_called_once()
            
            self.mod_b.return_value.pre_configure.assert_called_once()
            self.mod_b.return_value.configure.assert_called_once()
            self.assertFalse(hasattr(self.mod_b.return_value, 'post_configure'))
            
            # 验证日志仍然记录了所有阶段
            mock_logger.info.assert_any_call("开始执行阶段: configure")
            mock_logger.info.assert_any_call("开始执行阶段: post_configure")

    async def test_initialize_modules_with_async_error(self):
        # 准备模拟模块类
        for mod in [self.root_module, self.mod_a, self.mod_b, self.mod_c]:
            mod.return_value = Mock()
        
        # 设置一个异步方法抛出异常
        async def faulty_configure():
            raise ValueError("配置错误")
        
        self.mod_b.return_value.configure = faulty_configure

        with patch('pbd_core.ModuleManager.logger') as mock_logger:
            with self.assertRaises(ValueError) as context:
                await self.manager.initialize_modules()
            
            # 验证异常消息
            self.assertEqual(str(context.exception), "配置错误")
            
            # 验证日志记录了方法开始执行（因为错误发生在执行过程中）
            mock_logger.info.assert_any_call("开始执行阶段: configure")
            
            # 不应该有error日志，因为异常是直接抛出的
            mock_logger.error.assert_not_called()


if __name__ == '__main__':
    unittest.main()