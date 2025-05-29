from typing import Type, List, Set, Dict
import asyncio
from .base import PbdModuleBase
from .exceptions import ModuleLoadError
from ..logging import HasLogger


class ModuleManager(HasLogger):
    def __init__(self, root_module_cls: Type['PbdModuleBase']):
        """
        :param root_module_cls: 应用的根模块类，作为依赖收集的起点
        """
        super().__init__()
        self.root_module_cls = root_module_cls
        self._init_order: List[Type['PbdModuleBase']] = []  # 拓扑排序后的模块初始化顺序
        self._visited: Set[Type['PbdModuleBase']] = set()  # 已访问的模块集合，防止重复访问
        self._rec_stack: Set[Type['PbdModuleBase']] = set()  # 当前递归栈，用于检测循环依赖

    def _topo_sort(self, mod_cls: Type['PbdModuleBase']):
        """
        递归进行拓扑排序：
        - 遍历模块的所有依赖 (_deps)
        - 先递归排序依赖模块，再将自己加入初始化顺序列表
        - 如果检测到当前模块在递归栈中，说明存在循环依赖，抛出异常
        """
        if mod_cls in self._visited:
            self.logger.debug(f"模块 {mod_cls.__name__} 已经访问过，跳过")
            return
        if mod_cls in self._rec_stack:
            path = " -> ".join(m.__name__ for m in self._rec_stack)
            self.logger.error(f"检测到循环依赖: {path} -> {mod_cls.__name__}")
            raise ModuleLoadError(f"循环依赖检测到模块链路: {path} -> {mod_cls.__name__}")

        self.logger.debug(f"开始处理模块 {mod_cls.__name__}")
        self._rec_stack.add(mod_cls)

        for dep in getattr(mod_cls, '_deps', []):
            self.logger.debug(f"模块 {mod_cls.__name__} 依赖 {dep.__name__}")
            self._topo_sort(dep)

        self._rec_stack.remove(mod_cls)
        self._visited.add(mod_cls)
        self._init_order.append(mod_cls)
        self.logger.info(f"模块 {mod_cls.__name__} 添加到初始化顺序")

    def collect_and_sort(self) -> List[Type['PbdModuleBase']]:
        """
        从根模块开始，收集所有依赖模块并拓扑排序。

        :return: 按依赖顺序排序后的模块类列表
        """
        self.logger.info(f"开始收集模块依赖并拓扑排序，根模块: {self.root_module_cls.__name__}")
        self._init_order.clear()
        self._visited.clear()
        self._rec_stack.clear()

        self._topo_sort(self.root_module_cls)

        self.logger.info("模块拓扑排序完成，初始化顺序如下:")
        for mod_cls in self._init_order:
            self.logger.info(f" - {mod_cls.__name__}")

        return self._init_order

    async def initialize_modules(self) -> Dict[Type['PbdModuleBase'], 'PbdModuleBase']:
        """
        按拓扑排序的顺序，依次创建模块实例，并调用模块的三个初始化阶段：
        pre_configure -> configure -> post_configure

        支持模块的初始化方法为同步或异步，统一用 await 调用。

        :return: 模块类到模块实例的映射字典
        """
        self.logger.info("开始初始化模块")
        order = self.collect_and_sort()
        instances: Dict[Type['PbdModuleBase'], 'PbdModuleBase'] = {}

        for mod_cls in order:
            self.logger.info(f"实例化模块 {mod_cls.__name__}")
            instances[mod_cls] = mod_cls()

        for phase in ['pre_configure', 'configure', 'post_configure']:
            self.logger.info(f"开始执行阶段: {phase}")
            for mod_cls in order:
                instance = instances[mod_cls]
                method = getattr(instance, phase, None)
                if method:
                    self.logger.info(f"执行模块 {mod_cls.__name__} 的 {phase} 方法")
                    if asyncio.iscoroutinefunction(method):
                        await method()
                    else:
                        await asyncio.to_thread(method)

        self.logger.info("所有模块初始化完成")
        return instances
