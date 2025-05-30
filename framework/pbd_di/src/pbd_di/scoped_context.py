from contextlib import asynccontextmanager
from contextvars import ContextVar
import inspect
from typing import Any


class ScopedContext:
    """专门管理SCOPED作用域实例的生命周期"""
    def __init__(self):
        self._context = ContextVar("scoped_ctx", default={})
    
    def get(self, name: str) -> Any:
        """获取作用域实例"""
        return self._context.get().get(name)
    
    def set(self, name: str, instance: Any):
        """设置作用域实例"""
        current = self._context.get()
        self._context.set({**current, name: instance})
    
    @asynccontextmanager
    async def scope(self):
        """SCOPED作用域上下文"""
        token = self._context.set({})
        try:
            yield
        finally:
            instances = self._context.get()
            for inst in instances.values():
                if (close := getattr(inst, "close", None)) and callable(close):
                    result = close()
                    if inspect.isawaitable(result):
                        await result
            self._context.reset(token)
