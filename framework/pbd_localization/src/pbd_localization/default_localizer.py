from typing import List, Optional, Union
from .interfaces import ILocalizer
from .localization_resource import LocalizationResource


class DefaultLocalizer(ILocalizer):
    """
    默认本地化类，用于获取本地化字符串
    使用LocalizationResource类获取本地化字符串
    未来可通过替换该类实现数据库或其他方式获取本地化字符串
    """

    def get(self, path: Union[str, List[str]], default: Optional[str] = None) -> str:
        """
        获取本地化字符串
        :param keys: 字符串或字符串列表
        :param default: 默认值
        :return: 本地化字符串
        """
        return LocalizationResource.get(path, self.current_lang, default)
