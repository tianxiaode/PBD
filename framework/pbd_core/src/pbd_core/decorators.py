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
        # 复制扩展类的方法到目标类
        for name, attr in extension_cls.__dict__.items():
            # 跳过特殊方法和私有方法
            if name.startswith('__') and name.endswith('__'):
                continue
                
            # 如果是方法
            if callable(attr):
                # 保存原始方法（如果存在）
                if hasattr(target_cls, name):
                    # 保存为 _original_{name}
                    original = getattr(target_cls, name)
                    setattr(target_cls, f'_original_{name}', original)
                
                # 绑定新方法到目标类
                setattr(target_cls, name, lambda self, *args, **kwargs: attr(self, *args, **kwargs))
            else:
                # 添加类属性
                setattr(target_cls, name, attr)
        
        return extension_cls
    return decorator