from .interfaces import IDependencyBase
def injectable_extension(target_class, deps=None):
    """
    类扩展装饰器
    :param target_class: 要扩展的目标类
    :param deps: 新增依赖项列表 [Interface1, Interface2]
    """
    deps = deps or []
    
    def decorator(extension_module):
        # === 1. 直接添加新依赖到deps字典 ===
        if not  issubclass(target_class, IDependencyBase):
            raise TypeError(f"{target_class} 类必须是IDependencyBase的子类")
        
        if deps:
            # 确保目标类有deps属性
            if not hasattr(target_class, 'deps'):
                target_class.deps = {}
            
            for dep in deps:
                name = target_class._get_default_dependency_name(dep)
                target_class.deps[name] = dep
        
        # === 2. 添加/覆盖方法 ===
        for name in dir(extension_module):
            if name.startswith('__'):
                continue
                
            func = getattr(extension_module, name)
            if callable(func):
                setattr(target_class, name, func)
        
        return extension_module
    
    return decorator