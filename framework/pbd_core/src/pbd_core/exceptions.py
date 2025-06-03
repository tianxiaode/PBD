from typing import Optional

class PbdException(Exception):
    """pbd框架的异常基类"""

    def __init__(
            self, 
            message: str, 
            code: Optional[str] = None, 
            details: Optional[str] = None, 
            inner_exception: Optional[Exception] = None, 
            data: Optional[dict] = None,
        ):
        """
        :param message: 异常信息
        :param code: 异常码
        :param details: 异常详情
        :param inner_exception: 内部异常
        :param data: 异常数据
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details
        self.inner_exception = inner_exception
        self.data = data

    def __str__(self):
        dict = {
            "message": self.message,
            "code": self.code,
            "details": self.details,
            "inner_exception": str(self.inner_exception) if self.inner_exception else None,
            "data": self.data
        }
        return f"{self.__class__.__name__}: {dict}"
    
