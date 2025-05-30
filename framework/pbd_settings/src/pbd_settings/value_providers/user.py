from .base import SettingValueProviderBase, SettingDefinition
from ..interfaces import ISettingStore

class UserSettingsValueProvider(SettingValueProviderBase):
    _name = 'U'
    _deps = [ISettingStore]


    def initialize(self):
        """初始化"""
        self._store = self.get_dependency(ISettingStore)

    async def get(self, setting: SettingDefinition) -> any:
        """获取配置值"""
        return await self._store.get(setting, self._name)

    async def get_all(self, settings: list[SettingDefinition]) -> dict[str, any]:
        """获取所有配置值"""
        return await self._store.get_all(settings, self._name)