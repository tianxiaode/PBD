def get_subclasses(cls):
    subclasses = []
    for subcls in cls.__subclasses__():
        subclasses.append(subcls)
    return subclasses

def get_all_subclasses(cls):
    subclasses = []
    for subcls in cls.__subclasses__():
        subclasses.append(subcls)
        subclasses.extend(get_all_subclasses(subcls))  # 递归收集子类的子类
    return subclasses