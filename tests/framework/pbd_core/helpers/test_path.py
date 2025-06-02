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
    
    def test_normalize(self):
        """测试路径规范化"""
        # 测试相对路径
        rel_path = "dir/../file.txt"
        abs_path = PathHelper.normalize(rel_path)
        self.assertEqual(abs_path, str(Path(rel_path).resolve()))
        
        # 测试绝对路径
        abs_input = str(self.root_path / "dir" / "file.txt")
        self.assertEqual(PathHelper.normalize(abs_input), abs_input)
        
        # 测试跨平台路径
        win_path = "dir\\subdir\\file.txt"
        norm_path = PathHelper.normalize(win_path)
        self.assertEqual(norm_path, str(Path(win_path).resolve()))

    def test_exist(self):
        """测试is_exist方法"""
        test_dir = self.root_path / "test_dir"
        
        # 测试目录不存在且不创建
        self.assertFalse(PathHelper.exist(test_dir))
        
        # 测试目录不存在但要求创建
        self.assertTrue(PathHelper.exist(test_dir, auto_create=True))
        self.assertTrue(test_dir.exists())
        
        # 测试目录已存在
        self.assertTrue(PathHelper.exist(test_dir))
        
        # 测试路径是文件不是目录
        test_file = self.root_path / "test_file.txt"
        test_file.touch()
        with self.assertRaises(ValueError):
            PathHelper.exist(test_file)
        
        # 测试创建多级目录
        nested_dir = test_dir / "subdir" / "nested"
        self.assertTrue(PathHelper.exist(nested_dir, auto_create=True))
        self.assertTrue(nested_dir.exists())
        
        # 测试创建目录失败（无权限）
        if os.name == 'posix':  # Unix-like系统
            protected_dir = "/root/test_dir"
            with self.assertRaises(OSError):
                PathHelper.exist(protected_dir, auto_create=True)

    def test_exist_exceptions(self):
        """测试is_exist方法的异常抛出"""
        # 测试路径存在但不是目录的情况
        test_file = self.root_path / "test_file.txt"
        test_file.touch()
        
        with self.assertRaises(ValueError) as cm:
            PathHelper.exist(test_file)
        self.assertIn("不是目录", str(cm.exception))
        
        # 测试创建目录时的权限错误
        if os.name == 'posix':
            with tempfile.NamedTemporaryFile() as temp_file:
                # 尝试在文件路径下创建目录（应该失败）
                with self.assertRaises(OSError) as cm:
                    PathHelper.exist(Path(temp_file.name) / "subdir", auto_create=True)
                self.assertIn("无法创建目录", str(cm.exception))

    def test_is_exist_create_failure(self):
        """测试is_exist方法在创建目录时的异常情况"""
        test_dir = self.root_path / "new_dir"
        
        # 使用mock模拟mkdir抛出OSError
        with patch.object(Path, 'mkdir', side_effect=OSError("模拟创建目录失败")):
            with self.assertRaises(OSError) as cm:
                PathHelper.exist(test_dir, auto_create=True)
            
            # 验证异常消息格式是否正确
            self.assertIn("无法创建目录", str(cm.exception))
            self.assertIn("模拟创建目录失败", str(cm.exception))                

    def test_delete(self):
        """测试delete方法"""
        # 测试文件删除
        test_file = self.root_path / "test_file.txt"
        test_file.touch()
        PathHelper.delete(test_file)
        self.assertFalse(test_file.exists())
        
        # 测试空目录删除
        empty_dir = self.root_path / "empty_dir"
        empty_dir.mkdir()
        PathHelper.delete(empty_dir, recursive=False)
        self.assertFalse(empty_dir.exists())
        
        # 测试递归目录删除
        nested_dir = self.root_path / "nested"
        (nested_dir / "subdir").mkdir(parents=True)
        (nested_dir / "file.txt").touch()
        PathHelper.delete(nested_dir)
        self.assertFalse(nested_dir.exists())
        
        # 测试不存在的路径（应该静默返回）
        PathHelper.delete("/nonexistent/path")
        
        # 测试符号链接删除
        if os.name != 'nt':  # Windows符号链接需要特殊权限
            link_path = self.root_path / "link"
            target_path = self.root_path / "target"
            target_path.mkdir()
            os.symlink(target_path, link_path)
            PathHelper.delete(link_path)
            self.assertFalse(link_path.exists())
            self.assertTrue(target_path.exists())  # 只删除链接不删除目标

        # 测试权限错误（更精确的测试）
        if os.name == 'posix':
            protected_file = "/root/test_file"
            try:
                # 先尝试创建测试文件（可能需要sudo）
                Path(protected_file).touch(mode=0o400, exist_ok=True)
                with self.assertRaises(OSError) as cm:
                    PathHelper.delete(protected_file)
                self.assertIn("删除失败", str(cm.exception))
            finally:
                # 清理测试文件
                Path(protected_file).unlink(missing_ok=True)



    def test_delete_exceptions(self):
        """测试delete方法的异常抛出（使用模拟）"""
        # 测试文件删除失败
        test_file = self.root_path / "test_file.txt"
        test_file.touch()
        
        # 模拟unlink抛出异常
        with patch.object(Path, 'unlink', side_effect=OSError("模拟删除失败")):
            with self.assertRaises(OSError) as cm:
                PathHelper.delete(test_file)
            self.assertIn("模拟删除失败", str(cm.exception))
        
        # 测试目录删除失败
        test_dir = self.root_path / "test_dir"
        test_dir.mkdir()
        
        # 模拟rmdir抛出异常
        with patch.object(Path, 'rmdir', side_effect=OSError("模拟目录删除失败")):
            with self.assertRaises(OSError) as cm:
                PathHelper.delete(test_dir)
            self.assertIn("模拟目录删除失败", str(cm.exception))
        
        # 测试递归删除时子文件删除失败
        nested_dir = self.root_path / "nested"
        nested_file = nested_dir / "file.txt"
        nested_dir.mkdir()
        nested_file.touch()
        
        # 模拟iterdir返回包含文件的列表
        with patch.object(Path, 'iterdir', return_value=[nested_file]):
            # 模拟unlink抛出异常
            with patch.object(Path, 'unlink', side_effect=OSError("模拟子文件删除失败")):
                with self.assertRaises(OSError) as cm:
                    PathHelper.delete(nested_dir)
                self.assertIn("模拟子文件删除失败", str(cm.exception))


    
    def test_singleton(self):
        """测试单例模式"""
        instance1 = PathHelper()
        instance2 = PathHelper()
        self.assertIs(instance1, instance2)

if __name__ == '__main__':
    unittest.main()
