from abc import ABC, abstractmethod
from typing import Any, ClassVar, Optional

class SettingProvider(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self) -> dict[str, Any]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self, names: list[str]):
        raise NotImplementedError
