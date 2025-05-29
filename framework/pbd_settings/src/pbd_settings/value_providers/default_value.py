from .base import SettingValueProviderBase, SettingDefinition

class DefaultValueSettingValueProvider(SettingValueProviderBase):
    """默认值配置值提供者"""

    _name = 'D'

    async def get(self, setting: SettingDefinition) -> any:
        """获取配置值"""
        return setting.default_value

    async def get_all(self, settings: list[SettingDefinition]) -> dict[str, any]:
        """获取所有配置值"""
        return {setting.name: setting.default_value for setting in settings}