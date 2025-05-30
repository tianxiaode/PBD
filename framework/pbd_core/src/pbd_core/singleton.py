import threading


import threading

class SingletonBase:
    _instances = {}
    _init_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._init_lock:
                if cls not in cls._instances:
                    instance = super().__new__(cls)
                    instance._initialized = False
                    cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.initialize()

    def initialize(self):
        """子类应在此实现初始化逻辑"""
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if '__init__' in cls.__dict__:
            raise TypeError(f"禁止在子类 {cls.__name__} 中重写 __init__，请使用 initialize() 替代。")
