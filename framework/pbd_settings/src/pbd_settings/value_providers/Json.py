from .base import SettingValueProviderBase, SettingDefinition
from ..interfaces import IJsonSettingStore

class JsonSettingsValueProvider(SettingValueProviderBase):
    _name = 'J'

    _deps = [IJsonSettingStore]

    async def initialize(self):
        """初始化"""
        self._store = self.get_dependency(IJsonSettingStore)

    async def get(self, setting: SettingDefinition) -> any:
        """获取配置值"""
        return await self._store.get(self._name,setting)

    async def get_all(self, settings: list[SettingDefinition]) -> dict[str, any]:
        """获取所有配置值"""
        return await self._store.get_all(self._name,settings)        

