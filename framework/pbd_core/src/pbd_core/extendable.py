from typing import Any, Callable, Dict, List, Type


class Extendable:
    """
    支持通过扩展机制动态修改类行为的基类
    
    特性：
    - 可完全替换方法实现
    - 可包装增强现有方法
    - 精确控制应用到特定子类
    """    
    _extensions: Dict[Type['Extendable'], List[Callable]] = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        original_init = cls.__init__
        
        def __init_with_extensions(self, *args, **kwargs):
            original_init(self)
            self._apply_extensions(**kwargs)
            
        cls.__init__ = __init_with_extensions

    @classmethod
    def register(cls, target_type: Type['Extendable'] = None):
        def decorator(ext_func: Callable):
            target = target_type or cls
            Extendable._extensions.setdefault(target, []).append(ext_func)
            return ext_func
        return decorator

    def _apply_extensions(self, **kwargs):
        for base in type(self).__mro__:
            if base in Extendable._extensions:
                for ext in Extendable._extensions[base]:
                    ext(self, **kwargs)