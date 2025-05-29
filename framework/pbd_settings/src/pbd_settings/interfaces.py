from abc import ABC, abstractmethod
from typing import Any, Optional


class ISettingStore(ABC):

    @abstractmethod
    def get(self, name: str, provider_name:Optional[str] = None, provider_key:Optional[str] = None)->Any:
        """获取指定名称的设置值"""
        if name is None:
            raise ValueError("name不能为 None")
        raise NotImplementedError()
    
    @abstractmethod
    def get_all(self, names: list[str], provider_name:Optional[str] = None, provider_key:Optional[str] = None)->dict[str, Any]:
        """获取多个设置值"""
        if names is None:
            raise ValueError("names不能为 None")
        raise NotImplementedError()
