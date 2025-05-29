from typing import List, Type, ClassVar

class PbdModuleBase:
    """
    模块基类，用于构建模块化依赖系统。

    Attributes:
        _deps (List[Type['PbdModuleBase']]): 
            声明当前模块直接依赖的模块类列表。
            ⚠️ 注意：只需要声明“直接依赖”模块，传递依赖会由系统自动处理。
            ✅ 依赖列表中模块的顺序很重要：
            如果模块 A 依赖模块 B 和 C，且 B 必须在 C 之前初始化，
            则应声明为：_deps = [B, C]
    """
    # 声明当前模块直接依赖的模块类列表。
    # ⚠️ 注意：只需要声明“直接依赖”模块，传递依赖会由系统自动处理。
    # ✅ 依赖列表中模块的顺序很重要：
    #    如果模块 A 依赖模块 B 和 C，且 B 必须在 C 之前初始化，
    #    则应声明为：_deps = [B, C]
    _deps: ClassVar[List[Type['PbdModuleBase']]] = []

    async def pre_configure(self):
        pass

    async def configure(self):
        pass

    async def post_configure(self):
        pass
