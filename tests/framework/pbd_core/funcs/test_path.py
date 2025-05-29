import unittest
import os
import shutil
from unittest.mock import patch, mock_open
from pbd_core import find_project_root, detect_source_dirs, norm_path

class TestPathUtils(unittest.TestCase):
    def setUp(self):
        # 创建临时目录结构用于测试
        self.test_dir = os.path.abspath("test_temp_dir")
        os.makedirs(self.test_dir, exist_ok=True)
        
        # 模拟pyproject.toml内容
        self.pyproject_content = """
        [tool.hatch.build]
        include = ["src/backend", "src/frontend", "docs/conf.py"]
        """
        
        # 创建src目录结构
        os.makedirs(os.path.join(self.test_dir, "src", "backend"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "src", "frontend"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "src", "no_init"), exist_ok=True)
        
        # 创建__init__.py文件
        with open(os.path.join(self.test_dir, "src", "backend", "__init__.py"), "w") as f:
            f.write("")
        with open(os.path.join(self.test_dir, "src", "frontend", "__init__.py"), "w") as f:
            f.write("")
    
    def tearDown(self):
        # 清理测试目录
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_find_project_root_success(self):
        # 创建pyproject.toml
        with open(os.path.join(self.test_dir, "pyproject.toml"), "w") as f:
            f.write(self.pyproject_content)
        
        # 测试能找到项目根目录
        result = find_project_root(os.path.join(self.test_dir, "src", "backend"))
        self.assertEqual(result, self.test_dir)
    
    @patch('os.path.exists')
    @patch('os.path.dirname')
    def test_find_project_root_failure(self, mock_dirname, mock_exists):
        # 模拟所有路径都不存在 pyproject.toml
        mock_exists.return_value = False
        
        # 动态生成目录层级关系
        def dirname_side_effect(path):
            parts = path.replace('\\', '/').rstrip('/').split('/')
            if len(parts) <= 1:  # 根目录返回自身
                return path
            return '/'.join(parts[:-1]) or '/'
        
        mock_dirname.side_effect = dirname_side_effect
        
        with self.assertRaises(FileNotFoundError):
            find_project_root('D:/a/b/c')  # 使用正斜杠保持跨平台兼容


    def test_detect_source_dirs_with_hatch_config(self):
        # 创建pyproject.toml
        with open(os.path.join(self.test_dir, "pyproject.toml"), "w") as f:
            f.write(self.pyproject_content)
        
        # 测试能正确检测到源目录
        with patch('pbd_core.funcs.path.find_project_root', return_value=self.test_dir):
            result = detect_source_dirs()
            expected = [
                os.path.join(self.test_dir, "src", "backend"),
                os.path.join(self.test_dir, "src", "frontend")
            ]
            self.assertCountEqual(result, expected)
    
    def test_detect_source_dirs_with_fallback(self):
        # 创建没有hatch配置的pyproject.toml
        with open(os.path.join(self.test_dir, "pyproject.toml"), "w") as f:
            f.write("[tool.something]\nkey = 'value'")
        
        # 测试回退到__init__.py检测
        with patch('pbd_core.funcs.path.find_project_root', return_value=self.test_dir):
            result = detect_source_dirs()
            expected = [
                os.path.join(self.test_dir, "src", "backend"),
                os.path.join(self.test_dir, "src", "frontend")
            ]
            self.assertCountEqual(result, expected)
    
    def test_detect_source_dirs_no_src(self):
        # 创建没有src目录的项目
        no_src_dir = os.path.join(self.test_dir, "no_src_project")
        os.makedirs(no_src_dir, exist_ok=True)
        with open(os.path.join(no_src_dir, "pyproject.toml"), "w") as f:
            f.write("[tool.something]\nkey = 'value'")
        
        # 测试没有源目录的情况
        with patch('pbd_core.funcs.path.find_project_root', return_value=no_src_dir):
            result = detect_source_dirs()
            self.assertEqual(result, [])
    
    def test_norm_path(self):
        # 测试路径标准化
        test_cases = [
            ("./some/path", os.path.normpath(os.path.abspath("some/path"))),
            ("../parent/path", os.path.normpath(os.path.abspath(os.path.join("..", "parent", "path")))),
            ("/absolute/path", os.path.normpath(os.path.abspath("/absolute/path"))),
            ("C:\\Windows\\Path", os.path.normpath("C:\\Windows\\Path")),
            ("mixed\\path/with/different/slashes", os.path.normpath(os.path.abspath("mixed/path/with/different/slashes")))
        ]
        
        for input_path, expected in test_cases:
            with self.subTest(input_path=input_path):
                result = norm_path(input_path)
                self.assertEqual(result, expected)
    
    @patch('pbd_core.funcs.path.find_project_root')
    @patch('tomllib.load')
    @patch('builtins.open', new_callable=mock_open)
    def test_detect_source_dirs_with_mock(self, mock_file, mock_toml, mock_find_root):
        # 设置mock返回值
        mock_find_root.return_value = self.test_dir
        mock_toml.return_value = {
            "tool": {
                "hatch": {
                    "build": {
                        "include": ["src/backend", "src/frontend", "docs/conf.py"]
                    }
                }
            }
        }
        
        # 调用函数
        result = detect_source_dirs()
        
        # 验证mock调用
        mock_file.assert_called_once()
        mock_toml.assert_called_once()
        
        # 验证结果
        expected = [
            os.path.join(self.test_dir, "src", "backend"),
            os.path.join(self.test_dir, "src", "frontend")
        ]
        self.assertCountEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
