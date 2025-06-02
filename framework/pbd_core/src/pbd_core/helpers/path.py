import os
import sys
from pathlib import Path
from typing import Optional, Union

class PathHelper:
    _root: Optional[Path] = None
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def set_root(self, path: Union[str, Path]) -> None:
        """设置项目根路径"""
        path = Path(path).resolve()
        if not path.exists():
            raise ValueError(f"路径不存在: {path}")
        if not path.is_dir():
            raise ValueError(f"必须是一个目录: {path}")
        
        self._root = path
        # 添加到系统路径（可选）
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    
    @classmethod
    def get_root(self) -> Path:
        """获取项目根路径"""
        if self._root is None:
            # 尝试自动推断（常见位置）
            candidates = [
                Path.cwd(),  # 当前工作目录
                Path(__file__).parent.parent,  # 从模块文件推断
                Path(sys.argv[0]).parent  # 从执行文件推断
            ]
            
            for path in candidates:
                if (path / "src").exists() or (path / "requirements.txt").exists():
                    self.set_root(path)
                    break
            else:
                raise RuntimeError("项目根路径未设置且无法自动推断")
        return self._root
    
    @classmethod
    def get_src(self) -> Path:
        """获取源码目录路径"""
        return self.get_root() / "src"
    
    @classmethod
    def get_data(self) -> Path:
        """获取数据目录路径"""
        return self.get_root() / "data"
    
    @classmethod
    def get_config(self) -> Path:
        """获取配置目录路径"""
        return self.get_root() / "config"
    
    @classmethod
    def from_root(self, *subpaths) -> Path:
        """从根目录构建路径"""
        return self.get_root().joinpath(*subpaths)
    
    @classmethod
    def from_src(self, *subpaths) -> Path:
        """从源码目录构建路径"""
        return self.get_src().joinpath(*subpaths)
    
    @classmethod
    def normalize(self,path):
        """将路径转换为标准格式（跨平台兼容）"""
        return os.path.normpath(os.path.abspath(path))
    
    @classmethod
    def exist(self, path: Union[str, Path], auto_create: bool = False) -> bool:
        """
        检查目录是否存在，并根据参数决定是否创建
        
        参数:
            path: 要检查的目录路径
            auto_create: 如果为True，当目录不存在时自动创建
            
        返回:
            bool: 目录是否存在（或是否成功创建）
            
        异常:
            ValueError: 当路径存在但不是目录时
            OSError: 当创建目录失败时
        """
        path = Path(path) if isinstance(path, str) else path
        path = path.resolve()  # 解析为绝对路径
        
        if path.exists():
            if not path.is_dir():
                raise ValueError(f"路径存在但不是目录: {path}")
            return True
        
        if auto_create:
            try:
                path.mkdir(parents=True, exist_ok=True)
                return True
            except OSError as e:
                raise OSError(f"无法创建目录 {path}: {e}")
        
        return False  

    @classmethod
    def delete(self, path: Union[str, Path], recursive: bool = True) -> None:
        """
        删除文件或目录
        
        参数:
            path: 要删除的路径
            recursive: 是否递归删除目录内容，默认为True
            
        异常:
            ValueError: 当路径不存在时
            OSError: 删除操作失败时
        """
        path = Path(path) if isinstance(path, str) else path
        path = path.resolve()  # 解析符号链接
        
        if not path.exists():
            return  # 路径不存在，不做操作
        
        try:
            if path.is_file() or path.is_symlink():
                path.unlink()  # 删除文件或符号链接
            elif path.is_dir():
                if recursive:
                    # 递归删除子内容
                    for child in path.iterdir():
                        self.delete(child, recursive=True)
                # 删除目录本身
                path.rmdir()
        except OSError as e:
            raise OSError(f"删除失败 {path}: {e}")
        



