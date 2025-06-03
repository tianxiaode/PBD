from pbd_core import PbdException

class CircularDependencyException(PbdException):
    
    def __init__(self, name: str):
        code = 'app.circular_dependency'
        data = {'name': name}
        super().__init__(code, code=code, data=data)

class InvalidScopeException(PbdException):

    def __init__(self, target: type, scope: str):
        code = 'app.invalid_scope'
        data = {'target': target.__name__, 'scope': scope}
        super().__init__(code, code=code, data=data)    

class DependencyNotFoundException(PbdException):

    def __init__(self, target: type):
        code = 'app.dependency_not_found'
        data = {'target': target.__name__}
        super().__init__(code, code=code, data=data)

class InjectableExtensionInvalidTypeException(PbdException):

    def __init__(self, target: type):
        code = 'app.injectable_extension_invalid_type'
        data = {'target': target.__name__}
        super().__init__(code, code=code, data=data)