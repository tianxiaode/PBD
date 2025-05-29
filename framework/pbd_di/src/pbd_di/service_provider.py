from typing import Any, Type
from .interfaces import IServiceProvider
from .container import Container

class ServiceProvider(IServiceProvider):

    async def get(self, service_type: Type) -> Any:
        """从容器获取服务实例"""
        return await Container().get(service_type)