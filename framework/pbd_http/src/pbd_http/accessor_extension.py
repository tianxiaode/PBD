from typing import Dict, Callable, Type, Any, ClassVar

class AccessorExtension:
    """访问器扩展混入类"""
    _extensions: ClassVar[Dict[Type, Dict[str, Callable]]] = {}
    
    @classmethod
    def add_extension(cls, ext_name: str = None):
        """扩展方法装饰器"""
        def decorator(ext_func: Callable):
            name = ext_name or ext_func.__name__
            if cls not in cls._extensions:
                cls._extensions[cls] = {}
            cls._extensions[cls][name] = ext_func
            return ext_func
        return decorator
    
    @classmethod
    def apply_extensions(cls, request: Any, target_object: Any):
        """类方法：将扩展应用到目标对象"""
        for ext in cls._extensions.get(cls, {}).values():
            ext(cls, request, target_object)  # 传入类对象而非实例


# class CurrentUserAccessor(IHttpContextAccessor, AccessorExtension):
#     _injector_name = "current_user"
    
#     @classmethod
#     def get_instance(cls, request) -> 'CurrentUser':
#         user = CurrentUser(cls._extract_data(request))
#         cls.apply_extensions(request, user)  # 直接使用类方法
#         return user
    
#     @classmethod
#     def _extract_data(cls, request) -> Dict[str, Any]:
#         return {'id': request.user.id, 'name': request.user.username}


# @CurrentUserAccessor.add_extension()
# def load_permissions(accessor_cls, request, user):
#     """权限扩展"""
#     user.permissions = request.session.get('permissions', [])
#     user.is_admin = request.user.is_superuser