from abc import ABC, abstractmethod
from typing import ClassVar, Dict, Type

class IHttpContextAccessor(ABC):
    """HttpContext 访问器接口
        注意：
        - 所有子类必须在应用启动时导入！
        - 禁止在运行时动态注册/修改！
        - 违反约定可能导致线程安全问题！
    """
    _registry: list[Type['IHttpContextAccessor']] = []
    _excluded: set[Type['IHttpContextAccessor']] = set()

    # 注入名称
    _injector_name: ClassVar[str] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls is IHttpContextAccessor:
            return
        if cls._injector_name is None:
            raise ValueError(f"访问器类{cls.__name__}必须定义注入名称")
        if cls._injector_name in [c._injector_name for c in IHttpContextAccessor._registry]:
            raise ValueError(f"访问器类{cls.__name__}的注入名称{cls._injector_name}已被占用")
        IHttpContextAccessor._registry.append(cls)    
       

    @classmethod
    def get_instances(cls, request) -> Dict[str,Type]:
        """获取当前请求的 HttpContext 访问器实例"""
        injectors = {}
        for accessor_cls in cls.all():
            injectors[accessor_cls._injector_name] = accessor_cls.get_instance(request)
        return injectors

    @classmethod
    @abstractmethod
    def get_instance(self, request) -> 'IHttpContextAccessor':
        """获取当前请求的 HttpContext 访问器实例"""
        raise NotImplementedError()

    @classmethod
    def all(cls) -> list[Type['IHttpContextAccessor']]:
        return [c for c in IHttpContextAccessor._registry if c not in IHttpContextAccessor._excluded]

    @classmethod
    def exclude(cls, accessor_cls: Type['IHttpContextAccessor']):
        """显式排除某个 accessor 子类"""
        IHttpContextAccessor._excluded.add(accessor_cls)

    @classmethod
    def clear(cls):
        """清空所有注册/排除项（测试场景用）"""
        IHttpContextAccessor._registry.clear()
        IHttpContextAccessor._excluded.clear()
