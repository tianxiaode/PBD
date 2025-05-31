from abc import ABC, abstractmethod
from typing import Any, Type
from pbd_core import HasLogger
from .generic import TDependency, SINGLETON, TRANSIENT, SCOPED

class InterfaceBase:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # 跳过 InterfaceBase 自己
        if cls is InterfaceBase:
            return

        # 这个类是接口，什么都不做
        if cls.is_interface():
            return

        # 找出最接近的接口类，注册默认实现
        for base in cls.__mro__[1:]:
            if base.is_interface():
                base.__di_implementation__ = cls
                break

    @classmethod
    def is_interface(cls) ->bool:
        # 只把“直接继承 InterfaceBase”的类视为接口
        return InterfaceBase in cls.__bases__
    

class IDependencyBase(HasLogger):
    _di_scope = None  # 可被子类重写

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # 继承父类的依赖
        deps = {}
        for base in cls.__bases__:
            if hasattr(base, 'deps'):
                deps.update(base.deps)

        # 处理当前类的 _deps
        if hasattr(cls, '_deps'):
            for dep in getattr(cls, '_deps', []):
                name = cls._get_default_dependency_name(dep)
                deps[name] = dep
            delattr(cls, '_deps')  # 删除原始声明

        cls.deps = deps

    def __init__(self, **kwargs):
        # 赋值依赖实例
        for attr_name, dep in kwargs.items():
            setattr(self, attr_name, dep)

    @classmethod
    def _get_default_dependency_name(cls, dep_type: type) -> str:
        return f"{dep_type.__module__}.{dep_type.__qualname__}".lower()

    def get_dependency(self, dependency_type: Type[TDependency]) -> TDependency:
        name = self._get_default_dependency_name(dependency_type)
        if hasattr(self, "deps") and name in self.deps:
            return getattr(self, name)
        raise ValueError(f"未找到依赖： {dependency_type}")    
    
    
class ISingletonDependency(IDependencyBase):
    _di_scope = SINGLETON

class ITransientDependency(IDependencyBase):
    _di_scope = TRANSIENT

class IScopedDependency(IDependencyBase):
    _di_scope = SCOPED

class IServiceProvider(ITransientDependency,InterfaceBase, ABC):
    """服务提供者接口 (类似 .NET 的 IServiceProvider)"""

    @abstractmethod
    async def get(self, service_type: Type) -> Any:
        """获取指定类型的服务实例"""
        raise NotImplementedError()
   