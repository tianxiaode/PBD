from typing import ClassVar, Optional, Protocol
from pbd_core import extend_class
from pbd_di import IDependencyBase
from .interfaces import ILocalizer

extend_class(IDependencyBase)
class LocalizerExtension:
    """为注入类提供本地化服务的扩展类"""
    _resource_name: ClassVar[str] = None
    
    def t(self, key: str, default: Optional[str] = None):
        if self._localizer is None:
            self._localizer = self.get_dependency(ILocalizer)
        if self._resource_name is None:
            return self._localizer.get(key, default)
        return self._localizer.get(f"{self._resource_name}.{key}", default)
    
class Localizable:
    """为所有需要本地化的类提供基础功能"""
    def t(self, key: str, default: Optional[str] = None) -> str:
        """直接访问当前请求的本地化器"""
        # 动态获取已注入的本地化器实例
        if not hasattr(self, '_localizer'):
            self._localizer = self.get_dependency(ILocalizer)
        return self._localizer.t(key, default or key)