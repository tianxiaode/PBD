import logging
from .logger import Logger 

class HasLogger:
    @property
    def logger(self) -> logging.Logger:
        if not hasattr(self, '_logger'):
            setattr(self, '_logger', Logger.get_logger(self.__class__))
        return self._logger