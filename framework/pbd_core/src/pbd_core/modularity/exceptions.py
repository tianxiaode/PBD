from ..exceptions import PbdException

class ModuleLoadError(PbdException):
    """模块加载时抛出的异常，主要用于检测循环依赖"""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.code = "MODULE_LOAD_ERROR"
        self.details = "模块加载时发生错误，请检查模块间的依赖关系。"
        self.log_level = "ERROR"
