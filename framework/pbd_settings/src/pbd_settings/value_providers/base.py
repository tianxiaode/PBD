from abc import ABC, abstractmethod
from typing import Any, ClassVar
from pbd_di import ITransientDependency
from pbd_logging import HasLogger
from ..generic import SettingDefinition

class SettingValueProviderBase(ITransientDependency, HasLogger, ABC):
    """配置值提供者接口"""

    _name: ClassVar[str]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "_name") or not isinstance(cls._name, str) or not cls._name:
            raise TypeError(
                f"子类 {cls.__name__} 必须定义 class 属性 `_name`，且为非空字符串"
            )

    @abstractmethod
    async def get(self, Setting: SettingDefinition) -> Any:
        """获取配置值"""
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self, Settings: list[SettingDefinition]) -> dict[str, Any]:
        """获取多个配置值"""
        raise NotImplementedError()