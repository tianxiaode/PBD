from pbd_core import InternalException

class NotDependencyBaseSubclassException(InternalException):

    def __init__(self, target: type):
        code = 'Not dependency base subclass '
        data = {"target": target.__name__}
        message = f"目标类 {target.__name__} 必须是IependencyBase的的子类"
        super().__init__(message,code=code, data=data)

class ResourceNameDuplicateException(InternalException):

    def __init__(self, resource_name: str, target: type):
        code = 'Resource name duplicate '
        data = {"resource_name": resource_name, "target": target.__name__}
        message = f"资源名称 {resource_name} 已经存在于目标类 {target.__name__} 中"
        super().__init__(message,code=code, data=data)

class EmptyResourceNameException(InternalException):
    def __init__(self, cls_name: str):
        code = 'Empty resource name '
        data = {"class": cls_name}
        message = f"{cls_name} 必须设置非空的 resource_name"
        super().__init__(message,code=code, data=data)

class InvalidTextsFormatException(InternalException):
    def __init__(self, cls_name: str):
        code = 'Invalid texts format '
        data = {"class": cls_name}
        message = f"{cls_name} 必须设置 texts 字典"
        super().__init__(message,code=code, data=data)

class InvalidLanguageFormatException(InternalException):
    def __init__(self, cls_name: str):
        code = 'Invalid language format '
        data = {"class": cls_name}
        message = f"{cls_name} 的 texts 格式不正确，应为 {'语言代码': {'键': '翻译'}}"
        super().__init__(message,code=code, data=data)

class InvalidDefaultLanguageException(InternalException):
    def __init__(self):
        code = 'Invalid default language'
        message = "默认语言必须是非空字符串"
        super().__init__(message, code=code)