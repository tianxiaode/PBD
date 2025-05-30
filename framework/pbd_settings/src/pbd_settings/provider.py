from abc import ABC, abstractmethod
from typing import Any, Optional
from pbd_di import ITransientDependency
from .interfaces import ISettingValueProviderManager

class SettingProvider(ITransientDependency,ABC):

    _deps = [ISettingValueProviderManager]

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self) -> dict[str, Any]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self, names: list[str]):
        raise NotImplementedError
