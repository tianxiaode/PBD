from .base import SettingValueProviderBase, SettingDefinition


class UserSettingsValueProvider(SettingValueProviderBase):
    _name = 'U'

    async def get(self, setting: SettingDefinition) -> any:
        pass

    async def get_all(self, settings: list[SettingDefinition]) -> dict[str, any]:
        pass