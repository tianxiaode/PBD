from pbd_core import PbdException

class PbdAuthenticationError(PbdException):

    def __init__(self, data: dict):
        code = "app.authentication_error"
        super().__init__(code,code=code, data=data)
