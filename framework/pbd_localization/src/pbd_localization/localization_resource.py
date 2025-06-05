from typing import Dict, ClassVar, List, Type, Any, Union
from pbd_core import DictHelper
from .exceptions import (
    ResourceNameDuplicateException,
    EmptyResourceNameException,
    InvalidTextsFormatException,
    InvalidLanguageFormatException,
    InvalidDefaultLanguageException,
)


class LocalizationResource:
    """
    本地化资源管理
    约定：
    1. 资源定义时可使用嵌套字典结构
    2. 内部自动转换为扁平化存储
    3. 查询路径格式：<资源名称>.<扁平键名>
    
    示例：
    class CommonResources(LocalizationResource):
        resource_name = "common"
        texts = {
            "en": {
                "button": {
                    "submit": "Submit",
                    "cancel": "Cancel"
                },
                "header": {
                    "welcome": "Welcome, {username}!"
                }
            },
            "zh-CN": {
                "button": {
                    "submit": "提交",
                    "cancel": "取消"
                },
                "header": {
                    "welcome": "欢迎, {username}!"
                }
            }
        }
        
    内部扁平化存储：
    {
        "en": {
            "common.button.submit": "Submit",
            "common.button.cancel": "Cancel",
            "common.header.welcome": "Welcome, {username}!"
        },
        "zh-CN": {
            "common.button.submit": "提交",
            "common.button.cancel": "取消",
            "common.header.welcome": "欢迎, {username}!"
        }
    }
    
    查询示例：
    LocalizationResource.get("common.button.submit", "zh-CN")
    """
        

    _registry: ClassVar[Dict[str, Type["LocalizationResource"]]] = {}
    _public_registry: ClassVar[Dict[str, Type["LocalizationResource"]]] = {}
    texts: ClassVar[Dict[str, Dict]] = {}
    resource_name: ClassVar[str] = ""
    _default_lang: str = "en"
    is_public: ClassVar[bool] = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._validate_resource()

        if cls.resource_name:
            if cls.resource_name in cls._registry:
                raise ResourceNameDuplicateException(
                    cls.resource_name, LocalizationResource._registry[cls.resource_name]
                )
            LocalizationResource._registry[cls.resource_name] = cls
            if cls.is_public:
                LocalizationResource._public_registry[cls.resource_name] = cls
            cls._flatten_texts()

    @classmethod
    def get(cls, key: str, code: str, default: Any = None) -> Any:
        """获取指定路径的本地化文本"""

        return LocalizationResource._get_texts(code).get(key, None) or\
            LocalizationResource._get_texts(LocalizationResource.get_default_lang()).get(key, default)


    @classmethod
    def get_default_lang(cls) -> str:
        """获取默认语言"""
        return LocalizationResource._default_lang

    @classmethod
    def set_default_lang(cls, lang: str):
        """设置默认语言"""
        if not isinstance(lang, str) or not lang:
            raise InvalidDefaultLanguageException()
        LocalizationResource._default_lang = lang

    @classmethod
    def _get_texts(cls, code: str) -> Dict:
        """获取指定资源名称的本地化文本"""
        return LocalizationResource.texts.get(code, {})

    @classmethod
    def _validate_resource(cls):
        """验证资源类配置"""
        if not cls.resource_name:
            raise EmptyResourceNameException(cls.__name__)


    @classmethod
    def _flatten_texts(cls) -> None:
        """将嵌套文本转换为扁平化结构"""
        if not hasattr(cls, "texts") or not isinstance(cls.texts, dict):
            return {}

        flat_texts = {}
        resousce_name = cls.resource_name

        for lang, translations in cls.texts.items():
            # 验证语言代码
            if not isinstance(lang, str) or not lang:
                raise InvalidLanguageFormatException(cls.__name__, lang)

            # 扁平化处理
            flat_texts[lang] = DictHelper.flatten(translations, resousce_name)

        LocalizationResource.texts.update(flat_texts)
