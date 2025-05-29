from abc import abstractmethod
from uuid import UUID
from pbd_di import ISingletonDependency, InterfaceBase


class IGuidGenerator(ISingletonDependency, InterfaceBase):

    """GUID生成器接口

    该接口定义了GUID生成器的基本功能和特性。
    所有实现该接口的类都必须提供生成GUID的方法。
    """


    @abstractmethod
    def create(self,**kwargs) -> UUID:
        """生成一个新的GUID

        Returns:
            str: 生成的GUID字符串
        """
        raise NotImplementedError("Subclasses must implement this method")
