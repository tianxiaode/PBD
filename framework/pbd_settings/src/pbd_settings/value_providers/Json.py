from typing import Any
from .base import SettingValueProviderBase, SettingDefinition

class JsonSettingsValueProvider(SettingValueProviderBase):
    _name = 'J'

    async def get(self, setting: SettingDefinition) -> Any:
        """获取配置值"""
        pass

    async def get_all(self, settings: list[SettingDefinition]) -> dict[str, Any]:
        """获取所有配置值"""
        pass
        

