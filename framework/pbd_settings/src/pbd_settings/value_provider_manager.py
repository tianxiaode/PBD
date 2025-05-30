from typing import List
from .interfaces import ISettingValueProviderManager
from pbd_di import IServiceProvider
from pbd_core import PbdException
from .value_providers import SettingValueProviderBase
from .options import PbdSettingOptions

class SettingValueProviderManager(ISettingValueProviderManager):
    _deps=[IServiceProvider]

    def _get_providers(self) -> List[SettingValueProviderBase]:
        service_provider = self.get_dependency(IServiceProvider)
        duplicate_names = set()
        providers = []
        for type_ in PbdSettingOptions.value_providers:
            provider_name = getattr(type_, "_name", None)
            if not provider_name:
                raise PbdException(f"提供程序类型 {type_.__name__} 缺少 _name 属性")
            if provider_name in duplicate_names:
                raise PbdException(f"重复的设置值提供程序名称: {type_._name}，对应类型: {type_.__name__}")  
            duplicate_names.add(type_._name)
            providers.append(service_provider.get(type_))
        return providers
        
    