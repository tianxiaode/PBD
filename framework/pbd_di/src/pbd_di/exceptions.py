from pbd_core import InternalException

class CircularDependencyException(InternalException):
    
    def __init__(self, name: str):
        code = 'Circular dependency exception'
        data = {'name': name}
        message = f"检查到循环依赖： {name}"
        super().__init__(message, code=code, data=data)

class InvalidScopeException(InternalException):

    def __init__(self, target: type, scope: str):
        code = 'Invalid scope exception'
        data = {'target': target.__name__, 'scope': scope}
        message = f"无法解析 {target.__name__} 的作用域 {scope}"
        super().__init__(message, code=code, data=data)    

class DependencyNotFoundException(InternalException):

    def __init__(self, target: type):
        code = 'Dependency not found exception'
        data = {'target': target.__name__}
        message = f"无法解析 {target.__name__} 的依赖"
        super().__init__(message, code=code, data=data)

class InjectableExtensionInvalidTypeException(InternalException):

    def __init__(self, target: type):
        code = 'Injectable extension invalid type exception'
        data = {'target': target.__name__}
        message = f"Injectable extension {target.__name__} 必须是类"
        super().__init__(message, code=code, data=data)