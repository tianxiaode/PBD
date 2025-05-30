from pbd_core import PbdModuleBase
from .options import PbdSettingOptions
from .value_providers import DefaultValueSettingValueProvider, GlobalSettingsValueProvider, JsonSettingsValueProvider, UserSettingsValueProvider

class SettingsModule(PbdModuleBase):

     async def configure(self):
          PbdSettingOptions.add_value_provider(DefaultValueSettingValueProvider)
          PbdSettingOptions.add_value_provider(JsonSettingsValueProvider)
          PbdSettingOptions.add_value_provider(GlobalSettingsValueProvider)
          PbdSettingOptions.add_value_provider(UserSettingsValueProvider)