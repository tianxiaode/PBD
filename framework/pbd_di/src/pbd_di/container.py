import threading
import inspect
from typing import Dict, Any, List, Optional, Type
from contextvars import ContextVar
from .generic import SINGLETON, TRANSIENT, SCOPED
from pbd_core import HasLogger, SingletonBase
from .scoped_context import ScopedContext
from .exceptions import CircularDependencyException, InvalidScopeException
from .funcs import get_default_dependency_name

_creating_instances_ctx: ContextVar[set] = ContextVar("_creating_instances_ctx")
def get_creating_instances() -> set:
    try:
        return _creating_instances_ctx.get()
    except LookupError:
        s = set()
        _creating_instances_ctx.set(s)
        return s


class Container(SingletonBase,HasLogger):
    """
    依赖注入容器。
    """
    _singletons: Dict[str, Any] = {}      # 类属性，全局单例存储
    _threading_lock = threading.RLock()  # 类级别锁，确保多个方法共享
    _creating_lock = threading.RLock()  # 专用于循环依赖检测

    
    def initialize(self):
        self._scoped_context = ScopedContext()
        self.logger.debug("容器已初始化")

    async def get(self, target: Type, context_instances: Optional[Dict[str,Type]] = None) -> Any:
        """
        从容器中获取一个依赖实例。
        """
        creating_instances = get_creating_instances()
        
        if hasattr(target, "__di_implementation__") and target.__di_implementation__ is not None:
            return await self.get(target.__di_implementation__)

        name = f"{target.__module__}.{target.__qualname__}"

        if name in creating_instances:
            raise CircularDependencyException(name)

        new_creating_instances = creating_instances.copy()
        new_creating_instances.add(name)
        token = _creating_instances_ctx.set(new_creating_instances)

        try:
            scope = target._di_scope
            if scope == SINGLETON:
                with self._threading_lock:
                    if name not in self._singletons:
                        self._singletons[name] = await self._create_instance(target, context_instances)
                    return self._singletons[name]
            elif scope == SCOPED:
                instance = self._scoped_context.get(name)
                if instance is None:
                    instance = await self._create_instance(target, context_instances)
                    self._scoped_context.set(name, instance)
                return instance
            elif scope == TRANSIENT:
                return await self._create_instance(target, context_instances)
            else:
                raise InvalidScopeException(target, scope)
        finally:
            _creating_instances_ctx.reset(token)
        
    async def _create_instance(self, target: Type, context_instances: Optional[Dict[str,Type]] = None) -> Any:
        """
        基于注册表条目创建实例，实现全配置驱动的依赖注入。

        Args:
            name:  原始的依赖名称 (可能是 str 或 Type)。
            class_name: 依赖的完整类路径字符串。
            dependency_type: 依赖的注册信息。

        Returns:
            创建的依赖实例。
        """
        deps = target.deps or {}
        self.logger.debug(f"创建实例: {target.__name__}({deps})")
        ctor_args = {}
        if context_instances:
            for name,instance in context_instances.items():
                ctor_args[name] = instance
        for name, dep in deps.items():
            ctor_args[name] =  await self.get(dep, context_instances)
        # 3. 实例化对象
        instance = target(**ctor_args)

        # 4. 调用异步初始化方法 (如果存在)
        if hasattr(instance, "initialize") and callable(instance.initialize):
            if inspect.iscoroutinefunction(instance.initialize):
                await instance.initialize()
            else:
                instance.initialize()

        return instance
    
    async def shutdown(self):
        """清理所有单例资源"""
        for name, instance in list(self._singletons.items()):
            if hasattr(instance, "close") and callable(instance.close):
                if inspect.iscoroutinefunction(instance.close):  # 判断是否是异步方法
                    await instance.close()  # 异步调用
                else:
                    instance.close()  # 同步调用            
            del self._singletons[name]
            self.logger.debug(f"已清理单例: {name}")


