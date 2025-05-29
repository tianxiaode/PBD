
from .base import SettingValueProviderBase, SettingDefinition
class GlobalSettingsValueProvider(SettingValueProviderBase):
    _name = 'G'

    async def get(self, setting: SettingDefinition) -> any:
        """获取配置值"""
        pass

    async def get_all(self, settings: list[SettingDefinition]) -> dict[str, any]:
        """获取所有配置值"""
        pass