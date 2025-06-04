from typing import Any, Optional, Protocol, Type, runtime_checkable
from pbd_di import IDependencyBase
from .interfaces import ILocalizer
from .exceptions import NotDependencyBaseSubclassException

@runtime_checkable
class ILocalizableSupport(Protocol):
    """支持本地化能力的协议"""
    def get_dependency(self, interface: Type) -> Any: ...
    def t(self, key: str, default: Optional[str] = None) -> str: ...

    
class Localizable:
    """为所有需要本地化的类提供基础功能"""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # 检查当前被定义的子类（cls）是否继承自 IDependencyBase
        if not issubclass(cls, IDependencyBase):
            raise NotDependencyBaseSubclassException(cls)
        
    def t(self, key: str, default: Optional[str] = None) -> str:
        """直接访问当前请求的本地化器"""
        # 动态获取已注入的本地化器实例
       
        if not hasattr(self, '_localizer'):
            self._localizer = self.get_dependency(ILocalizer)
        return self._localizer.t(key, default or key)