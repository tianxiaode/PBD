import threading
from typing import Dict,  Optional
from .generic import CultureInfo

class DefaultCulture:
    """
    默认文化类，用于管理默认文化数据
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._cultures = {}
                cls._instance._default_code = None
        return cls._instance

    def add(self, data: CultureInfo):
        """
        添加或更新文化信息。
        """
        code = data.language_code
        self._cultures[code] = data
        if self._default_code is None:
            self._default_code = code

    def get(self, code: str) -> Optional[CultureInfo]:
        return self._cultures.get(code)
    
    def get_all(self) -> Dict[str, 'CultureInfo']:
        return self._cultures    
    
    def remove(self, code: str):
        if code in self._cultures:
            del self._cultures[code]
        if self._default_code == code:
            self._default_code = None if not self._cultures else next(iter(self._cultures.keys()))

    def set_default(self, code: str):
        self._default_code = code
    
    def get_default(self) -> Optional[CultureInfo]:
        return self._cultures.get(self._default_code)
    
    def has (self, code: str) -> bool:
        return code in self._cultures