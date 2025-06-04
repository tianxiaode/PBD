from pbd_core import InternalException

class NotDependencyBaseSubclassException(InternalException):

    def __init__(self, target: type):
        message = f"目标类 {target.__name__} 必须是IependencyBase的的子类"
        super().__init__(message)