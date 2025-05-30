from .base import SettingValueProviderBase, SettingDefinition
from ..interfaces import IJsonSettingStore

class DefaultValueSettingValueProvider(SettingValueProviderBase):
    """默认值配置值提供者"""
    _deps = [IJsonSettingStore]
    _name = 'D'

    def initialized(self):
        self._store = self.get_dependency(IJsonSettingStore)


    async def get(self, setting: SettingDefinition, **kwargs) -> any:
        """获取配置值"""
        return self._store.get(setting)

    async def get_all(self, settings: list[SettingDefinition], **kwargs) -> dict[str, any]:
        """获取所有配置值"""
        return self._store.get_all(settings)