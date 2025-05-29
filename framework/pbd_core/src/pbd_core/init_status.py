
class InitStatusBase:
    """
        初始化状态基类
        说明：
            该类用于判断是否已经初始化，派生类可根据该属性判断类是否采用了单例模式，并根据情况决定是否重新初始化
    """
    def should_initialize(self) -> bool:
        """
            判断是否已经初始化
            说明：
                派生类可根据该属性判断类是否采用了单例模式，并根据情况决定是否重新初始化
            :return: bool
        """
        return not getattr(self, "_initialized", False)

    def mark_initialized(self):
        """
            设置初始化状态
            说明：
                单例模式类用于设置初始化状态，避免多重继承单例模式重复执行初始化
            :return: None
        """
        self._initialized = True


