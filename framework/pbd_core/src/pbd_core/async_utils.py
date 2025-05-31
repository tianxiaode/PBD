import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar('T')

class AsyncUtils:
    """异步工具集，用于统一接口"""
    _none_cache = None
    
    @classmethod
    def completed(cls):
        if cls._none_cache is None:
            fut = asyncio.Future()
            fut.set_result(None)
            cls._none_cache = fut
        return cls._none_cache    

    @staticmethod
    def result(value: T) -> asyncio.Future[T]:
        """带返回值的已完成任务"""
        fut = asyncio.Future()
        fut.set_result(value)
        return fut
    
    @staticmethod
    def error(ex: Exception) -> asyncio.Future:
        """带异常的任务"""
        fut = asyncio.Future()
        fut.set_exception(ex)
        return fut
    
    @staticmethod
    def run_sync(func: Callable, *args) -> asyncio.Future:
        """将同步函数包装为异步任务"""
        fut = asyncio.Future()
        try:
            result = func(*args)
            fut.set_result(result)
        except Exception as e:
            fut.set_exception(e)
        return fut
    
    @staticmethod
    def run_in_executor(func: Callable, *args) -> Awaitable:
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, func, *args)
