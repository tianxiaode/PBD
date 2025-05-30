from abc import ABC, abstractmethod
from typing import Any, Optional
from pbd_di import ISingletonDependency, InterfaceBase,ITransientDependency
from .value_providers import SettingValueProviderBase
from .schema import SettingDefinition

class ISettingStoreBase(ABC):

    @abstractmethod
    def get(self, setting: SettingDefinition, provider_name: Optional[str] = None, provider_key: Optional[str] = None)->Any:
        """获取指定名称的设置值"""
        raise NotImplementedError()
    
    @abstractmethod
    def get_all(self,settings: list[SettingDefinition], provider_name: Optional[str] = None, provider_key: Optional[str] = None)->dict[str, Any]:
        """获取多个设置值"""
        raise NotImplementedError()
    
class IJsonSettingStore(ISettingStoreBase, ISingletonDependency, InterfaceBase):
    pass

class ISettingStore(ISettingStoreBase, ITransientDependency, InterfaceBase):
    pass


class ISettingValueProviderManager(ISingletonDependency, InterfaceBase, ABC):


    @property
    def providers(self) -> list[SettingValueProviderBase]:
        if self._providers is None:
            self._providers = self._get_providers()
        return self._providers
    

    @abstractmethod    
    def _get_providers(self):
        raise NotImplementedError()
    