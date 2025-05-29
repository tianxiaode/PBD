

from enum import Enum
from typing import Any, Optional, Union
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

    @field_validator("type", mode='before')
    def normalize_type(cls, v):
        # 如果传的是 Python 类型对象，如 int、str、bool，转换成字符串
        if isinstance(v, type):
            return v.__name__
        return v