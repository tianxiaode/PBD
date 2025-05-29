from typing import ClassVar, Dict, Optional
from .generic import SettingDefinition

class SettingDefinitionProvider:
    group_name: ClassVar[str] = ""
    settings: ClassVar[list[SettingDefinition]] = []
    
    _registry: Dict[str, SettingDefinition] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        for setting in cls.settings:
            if isinstance(setting, SettingDefinition) is False:
                raise TypeError(f"设置定义必须是 SettingDefinition 类型: {setting}")
            key = f"{cls.group_name}.{setting.name}"
            if key in SettingDefinitionProvider._registry:
                raise ValueError(f"重复设置定义：{key}")
            SettingDefinitionProvider._registry[key] = setting

    @classmethod
    def get_settings(cls) -> Dict[str, SettingDefinition]:
        return SettingDefinitionProvider._registry
    
    @classmethod
    def get_setting(cls, name: str)->Optional[SettingDefinition]:
        return SettingDefinitionProvider._registry.get(name, None)


