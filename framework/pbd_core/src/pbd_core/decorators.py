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
    # 需要跳过的关键魔术方法
    SKIP_METHODS = {'__init__', '__new__', '__del__'}
    # 需要跳过的特殊属性
    SKIP_ATTRIBUTES = {'__dict__', '__class__', '__slots__', '__weakref__', '__module__'}

    def decorator(extension_cls):
        for name, attr in extension_cls.__dict__.items():
            # 跳过名称重整属性 (如 __private)
            if name.startswith(f'_{extension_cls.__name__}__'):
                continue
                
            # 跳过关键魔术方法
            if name in SKIP_METHODS:
                continue
                
            # 跳过特殊属性
            if name in SKIP_ATTRIBUTES:
                continue
                
            # 处理可调用对象（方法）
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
            
            # 处理非可调用属性
            else:
                setattr(target_cls, name, attr)
        
        return extension_cls
    return decorator