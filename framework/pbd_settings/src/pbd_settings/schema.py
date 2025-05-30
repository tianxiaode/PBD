from typing import ClassVar, Dict, Optional, Union,Any, List
from pydantic import BaseModel, field_validator

class SettingDefinition(BaseModel):
    name: str   
    type: Union[str, type] 
    display_name: Optional[str] = None
    default_value: Optional[Any] = None
    description: Optional[str] = None
    is_visible_to_client: bool = True
    providers: Optional[list[str]] = None
    is_inherited: bool = False
    is_encrypted: bool = False
    key: Optional[str] = None

    @field_validator("type", mode='before')
    def normalize_type(cls, v):
        # 如果传的是 Python 类型对象，如 int、str、bool，转换成字符串
        if isinstance(v, type):
            return v.__name__
        return v
    
class SettingGroup:
    def __init__(self, name: str, children: List[Union['SettingGroup', SettingDefinition]]):
        self.name = name
        self.children = children

    def flatten(self, parent_prefix="") -> List[tuple[str, SettingDefinition]]:
        entries = []
        prefix = f"{parent_prefix}.{self.name}" if parent_prefix else self.name
        for child in self.children:
            if isinstance(child, SettingDefinition):
                entries.append((f"{prefix}.{child.name}", child))
            elif isinstance(child, SettingGroup):
                entries.extend(child.flatten(prefix))
            else:
                raise TypeError(f"不支持的子节点类型: {type(child)}")
        return entries

class SettingSchema:
    settings: ClassVar[list[Union[SettingGroup, SettingDefinition]]] = []

    _registry: Dict[str, SettingDefinition] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        for item in cls.settings:
            if isinstance(item, SettingGroup):
                entries = item.flatten()
            elif isinstance(item, SettingDefinition):
                entries = [(item.name, item)]
            else:
                raise TypeError(f"不支持的设置类型: {type(item)}")

            for key, setting in entries:
                if key in SettingSchema._registry:
                    raise ValueError(f"重复设置定义：{key}")
                setting.key = key  # 💡 设置完整路径 key 到 setting
                SettingSchema._registry[key] = setting

    @classmethod
    def get_settings(cls) -> Dict[str, SettingDefinition]:
        return dict(SettingSchema._registry)

    @classmethod
    def get_setting(cls, name: str) -> Optional[SettingDefinition]:
        return SettingSchema._registry.get(name)

