from typing import Dict, ClassVar, List, Type, Any, Union
import warnings

class LocalizationResource:
    """
    本地化资源
    用于管理和获取多语言文本资源。
    通过子类化此类，可以定义不同的本地化资源。
    子类需要定义 resource_name 类变量，用于标识资源名称。
    子类需要定义 texts 类变量，用于存放多语言文本资源。
    子类可以定义 get_translations 方法，用于获取多语言文本资源。
    可直接在text中定义语言文本，如：
    texts = {
        'en': { 'hello': 'Hello', 'goodbye': 'Goodbye' },
        'zh-CN': { 'hello': '你好', 'goodbye': '再见' }
    }
    也可以通过导入方式知道文本词典，如：
    from my_app.resources.en import en_dict
    from my_app.resources.zh_cn import zh_cn_dict
    texts = {
        'en': en_dict,
        'zh-CN': zh_cn_dict
    }    
    默认语言设置：
    通过 set_default_lang() 设置全局默认语言，只能通过基类设置
    通过 get_default_lang() 获取当前默认语言    
    """
    _registry: ClassVar[Dict[str, Type['LocalizationResource']]] = {}
    texts: ClassVar[Dict[str, Dict]] = {}
    resource_name: ClassVar[str] = ""
    _default_lang: str = "en" 

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._validate_resource()
        cls._validate_texts()
            
        if cls.resource_name:            
            if cls.resource_name in cls._registry:
                raise ValueError(f"资源名称重复: {cls.resource_name}")
            cls._registry[cls.resource_name] = cls

    @classmethod
    def get(cls,path: str,code: str,default: Any = None) -> Any:
        """获取指定路径的本地化文本"""
        parts = path.split('.')
        if len(parts) < 2:
            return default
        resource_name, *keys = parts
        lang_dict = cls._get_texts(resource_name, code)
        if not lang_dict:
            return default
        # 逐级查找
        result = lang_dict
        for key in keys:
            if not isinstance(result, dict):
                return default
            result = result.get(key)
        return result if result is not None else default
    
    @classmethod
    def get_by_resource_name(cls, resource_name: str, code: str, keys: Union[str, List[str]], default: Any = None) -> Any:
        """获取指定资源名称的本地化文本"""
        if isinstance(keys, list):
            keys = '.'.join(keys)

        return cls.get(f"{resource_name}.{keys}", code, default)


    @classmethod
    def get_resource(cls, resource_name: str, code: str) -> Dict[str, Any]:
        """获取指定资源名称的本地化文本"""
        resource = cls._registry.get(resource_name)
        if not resource:
            return {}
        return resource.texts.get(code, {})
    
    @classmethod
    def get_resources(self, code: str)->Dict[str, Dict[str, Dict]]:
        """获取所有注册的资源"""
        resources = {}
        for resource_name in self._registry.keys():
            resources[resource_name] = self._get_texts(resource_name, code) or {}
        return resources
    
    @classmethod
    def get_default_lang(cls) -> str:
        """获取默认语言"""
        return LocalizationResource._default_lang

    @classmethod
    def set_default_lang(cls, lang: str):
        """设置默认语言"""
        if cls is not LocalizationResource:
            raise AttributeError("只能在 LocalizationResource 基类设置默认语言")
        if not isinstance(lang, str) or not lang:
            raise ValueError("默认语言必须是非空字符串")
        cls._default_lang = lang
    
    @classmethod
    def _get_texts(cls, resource_name: str, code: str) -> Dict[str, Dict]:
        """获取指定资源名称的本地化文本"""
        resource = cls._registry.get(resource_name)
        if not resource:
            return {}
        return resource.texts.get(code) or resource.texts.get(LocalizationResource._default_lang, {})
    
    @classmethod
    def _validate_resource(cls):
        """验证资源类配置"""
        if not cls.resource_name:
            raise ValueError(f"{cls.__name__} 必须设置非空的 resource_name")
        

    @classmethod
    def _validate_texts(cls):
        """验证texts配置"""
        if not isinstance(cls.texts, dict):
            raise ValueError(f"{cls.__name__} 必须设置 texts 字典")
        for lang, translations in cls.texts.items():
            if not isinstance(lang, str) or not isinstance(translations, dict):
                raise ValueError(f"{cls.__name__} 的 texts 格式不正确，应为 {'语言代码': {'键': '翻译'}}")

