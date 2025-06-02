
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
from pbd_di import ITransientDependency,IReplaceableInterface
from .generic import CultureInfo

class ICultureStore(ITransientDependency, IReplaceableInterface, ABC):
    """文化配置存储抽象接口"""
    @abstractmethod
    def get_all(self) -> Dict[str, 'CultureInfo']:
        pass
    
    @abstractmethod
    def get(self, code: str) -> Optional['CultureInfo']:
        pass
    
    @abstractmethod
    def add(self, culture: 'CultureInfo') -> None:
        pass
    
    @abstractmethod
    def remove(self, code: str) -> bool:
        pass
    
    @abstractmethod
    def set_default(self, code: str) -> None:
        pass
    
    @abstractmethod
    def get_default(self) -> Optional['CultureInfo']:
        pass

    @abstractmethod
    def has(self) -> bool:
        pass



class ILocalizer(ITransientDependency,IReplaceableInterface,ABC):

    def set_current_lang(self, lang: str) -> None:
        """设置当前语言"""
        self._current_lang = lang

    @property
    def current_lang(self) -> str:
        """获取当前语言"""
        return self._current_lang

    @abstractmethod
    def get(self, keys: Union[str, List[str]],default: Optional[str] = None) -> str:
        """获取本地化字符串"""
        pass

# class BaseController:
#     def __init__(self):
#         self.current_lang: str = "en"
#         self.localization_service = None  # 由外部注入

#     def set_current_lang(self, lang: str):
#         self.current_lang = lang

#     def get_text(self, path: str, default=None):
#         if not self.localization_service:
#             return default
#         return self.localization_service.get(path, self.current_lang, default)

#controller = await Container().get(route_info.controller)

# 注入请求和当前语言
# lang = (
#     request.args.get("lang") or
#     request.cookies.get("lang") or
#     request.headers.get("Accept-Language") or
#     "en"
# ).split(",")[0].strip()

# controller.set_current_lang(lang)
#  localization_service = await Container().get(ILocalizationService)  # 或从 DI 容器获取
# localization_service.set_current_lang(lang)
# controller.localization_service = localization_service  # 或从 DI 容器获取
#
