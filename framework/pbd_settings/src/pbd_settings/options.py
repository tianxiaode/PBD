
from typing import List
from .value_providers import SettingValueProviderBase


class PbdSettingOptions:

    _value_providers: List[SettingValueProviderBase] = []


    @classmethod
    def add_value_provider(cls, value_provider: SettingValueProviderBase) -> None:
        """添加配置值提供者"""
        if value_provider in cls._value_providers:
            return
        if not isinstance(value_provider, SettingValueProviderBase):
            raise TypeError(f"值提供者必须是 SettingValueProviderBase 的子类，不能是 {type(value_provider)}")
        cls._value_providers.append(value_provider)

    @property
    def value_providers(self) -> List[SettingValueProviderBase]:
        """获取当前配置值提供者列表"""
        return self._value_providers


