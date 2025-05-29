import threading
from.init_status import InitStatusBase

class SingletonBase(InitStatusBase):
    """单例基类"""
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__new__(cls)
                instance.mark_initialized()
                cls._instances[cls] = instance
        return cls._instances[cls]
