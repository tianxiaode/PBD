from ..options import PbdSettingOptions
from pbd_di import IServiceProvider, ISingletonDependency
from pbd_core import PbdException

class SettingValueProviderManager(ISingletonDependency):
    _deps =[IServiceProvider]

    async def initialize(self):
        self.service_provider = self.get_dependency(IServiceProvider)
        self.options = PbdSettingOptions
        self._providers = None  # Lazy cache

    @property
    def providers(self):
        if self._providers is None:
            self._providers = self._get_providers()
        return self._providers

    def _get_providers(self):
        duplicate_names = set()
        providers = []
        for type_ in self.options.value_providers:
            provider_name = getattr(type_, "_name", None)
            if not provider_name:
                raise PbdException(f"提供程序类型 {type_.__name__} 缺少 _name 属性")
            if provider_name in duplicate_names:
                raise PbdException(f"重复的设置值提供程序名称: {type_._name}，对应类型: {type_.__name__}")  
            duplicate_names.add(type_._name)
            providers.append(self.service_provider.get(type_))
        return providers
