from typing import Optional


class PbdException(Exception):
    """pbd框架的异常基类"""

    def __init__(
            self, 
            message: str, 
            code: Optional[str] = None, 
            details: Optional[str] = None, 
            inner_exception: Optional[Exception] = None, 
            log_level: Optional[str] = None,
        ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details
        self.inner_exception = inner_exception
        self.log_level = log_level

    def __str__(self):
        dict = {
            "message": self.message,
            "code": self.code,
            "details": self.details,
            "inner_exception": str(self.inner_exception) if self.inner_exception else None,
            "log_level": self.log_level,
        }
        return f"{self.__class__.__name__}: {dict}"