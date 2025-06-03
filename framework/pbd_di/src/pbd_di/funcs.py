def replace_service(source: type, target: type):
    """
    替换服务
    可以使用此函数将目标服务类型的实现替换为源服务类型的实现。
    :param source: 源服务类型
    :param target: 目标服务类型
    :return: None
    """
    if source is None or target is None:
        raise TypeError("源服务类型和目标服务类型不能为空")
    if not isinstance(source, type) or not isinstance(target, type):
        raise TypeError("源服务类型和目标服务类型必须是类型")
    
    setattr(target, '__di_implementation__', source)

def get_default_dependency_name(target: type):
    """
    获取默认依赖名称
    :param target: 服务类型
    :return: 字符串，默认依赖名称
    """
    return f"{target.__module__}.{target.__qualname__}".lower()
