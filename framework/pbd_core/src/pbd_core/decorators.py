def extend_class(target_cls):
    """
    类扩展装饰器 - 直接在运行时增强类方法
    用法:
        @extend_class(MyClass)
        class MyExtensions:
            def new_method(self):
                ...
            
            def existing_method(self):
                # 增强原有方法
                ...
    """
    def decorator(extension_cls):
        for name, attr in extension_cls.__dict__.items():
            # 跳过魔术方法 (__init__等) 但保留自定义方法 (如 __custom__)
            if name.startswith('__') and name.endswith('__') and name not in extension_cls.__dict__:
                continue
                
            # 处理方法和函数
            if callable(attr):
                # 创建闭包捕获当前attr值
                def make_wrapper(wrapped_func):
                    def wrapper(self, *args, **kwargs):
                        return wrapped_func(self, *args, **kwargs)
                    return wrapper
                
                wrapper_func = make_wrapper(attr)
                
                # 保存原始方法
                if hasattr(target_cls, name):
                    original = getattr(target_cls, name)
                    setattr(target_cls, f'_original_{name}', original)
                
                # 绑定新方法
                setattr(target_cls, name, wrapper_func)
            
            # 处理属性（排除模块级属性）
            elif not name.startswith('__') or not hasattr(extension_cls, '__module__'):
                setattr(target_cls, name, attr)
        
        return extension_cls
    return decorator