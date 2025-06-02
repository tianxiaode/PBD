import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch
from pbd_core import PathHelper

class TestPathHelper(unittest.TestCase):
    """PathHelper 单元测试"""
    
    def setUp(self):
        """测试前重置单例状态"""
        PathHelper._root = None
        PathHelper._instance = None
        
        # 创建临时目录结构
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name)
        
        # 创建标准子目录
        (self.root_path / "src").mkdir()
        (self.root_path / "data").mkdir()
        (self.root_path / "config").mkdir()
        (self.root_path / "requirements.txt").touch()
    
    def tearDown(self):
        """测试后清理临时目录"""
        self.temp_dir.cleanup()
    
    def test_set_root(self):
        """测试设置根路径"""
        # 测试有效路径
        PathHelper.set_root(self.root_path)
        self.assertEqual(PathHelper._root, self.root_path.resolve())
        
        # 测试字符串路径
        PathHelper.set_root(str(self.root_path))
        self.assertEqual(PathHelper._root, self.root_path.resolve())
        
        # 测试无效路径
        with self.assertRaises(ValueError):
            PathHelper.set_root("/nonexistent/path")
        
        # 测试非目录路径
        file_path = self.root_path / "file.txt"
        file_path.touch()
        with self.assertRaises(ValueError):
            PathHelper.set_root(file_path)
    
    def test_get_root(self):
        """测试获取根路径"""
        # 测试手动设置
        PathHelper.set_root(self.root_path)
        self.assertEqual(PathHelper.get_root(), self.root_path.resolve())
        
        # 测试自动推断（通过setUp创建的临时目录结构）
        PathHelper._root = None
        with patch('sys.argv', ['dummy_script.py']), \
             patch('os.getcwd', return_value=str(self.root_path)):
            inferred_root = PathHelper.get_root()
            self.assertEqual(inferred_root, self.root_path.resolve())
        
        # 测试无法推断的情况
        PathHelper._root = None
        with patch('sys.argv', ['dummy_script.py']), \
             patch('os.getcwd', return_value='/tmp'), \
             self.assertRaises(RuntimeError):
            PathHelper.get_root()
    
    def test_get_src_data_config(self):
        """测试获取标准子目录"""
        PathHelper.set_root(self.root_path)
        
        self.assertEqual(PathHelper.get_src(), self.root_path / "src")
        self.assertEqual(PathHelper.get_data(), self.root_path / "data")
        self.assertEqual(PathHelper.get_config(), self.root_path / "config")
    
    def test_from_root(self):
        """测试从根目录构建路径"""
        PathHelper.set_root(self.root_path)
        
        test_path = PathHelper.from_root("dir1", "dir2", "file.txt")
        expected = self.root_path / "dir1" / "dir2" / "file.txt"
        self.assertEqual(test_path, expected)
        
        # 测试空参数
        self.assertEqual(PathHelper.from_root(), self.root_path)
    
    def test_from_src(self):
        """测试从源码目录构建路径"""
        PathHelper.set_root(self.root_path)
        
        test_path = PathHelper.from_src("module", "submodule.py")
        expected = self.root_path / "src" / "module" / "submodule.py"
        self.assertEqual(test_path, expected)
        
        # 测试空参数
        self.assertEqual(PathHelper.from_src(), self.root_path / "src")
    
    def test_norm_path(self):
        """测试路径规范化"""
        # 测试相对路径
        rel_path = "dir/../file.txt"
        abs_path = PathHelper.norm_path(rel_path)
        self.assertEqual(abs_path, str(Path(rel_path).resolve()))
        
        # 测试绝对路径
        abs_input = str(self.root_path / "dir" / "file.txt")
        self.assertEqual(PathHelper.norm_path(abs_input), abs_input)
        
        # 测试跨平台路径
        win_path = "dir\\subdir\\file.txt"
        norm_path = PathHelper.norm_path(win_path)
        self.assertEqual(norm_path, str(Path(win_path).resolve()))
    
    def test_singleton(self):
        """测试单例模式"""
        instance1 = PathHelper()
        instance2 = PathHelper()
        self.assertIs(instance1, instance2)

if __name__ == '__main__':
    unittest.main()
