from pathlib import Path
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
    
    def test_find_project_root(self):
        """测试所有可能的sys.modules情况"""
        test_cases = [
            # 情况1: 正常有__main__模块且有__file__
            {
                "name": "with_main_module",
                "mock_modules": {"__main__": type("", (), {"__file__": str(Path(self.test_dir)/"main.py")})},
                "expected": Path(self.test_dir).resolve()
            },
            # 情况2: 有__main__模块但无__file__
            {
                "name": "main_module_no_file", 
                "mock_modules": {"__main__": object()},  # 普通object没有__file__
                "expected": Path.cwd().resolve()
            },
            # 情况3: 无__main__模块
            {
                "name": "no_main_module",
                "mock_modules": {},
                "expected": Path.cwd().resolve() 
            },
            # 情况4: __main__模块为None
            {
                "name": "main_module_is_none",
                "mock_modules": {"__main__": None},
                "expected": Path.cwd().resolve()
            }
        ]

        for case in test_cases:
            with self.subTest(case["name"]):
                with patch('sys.modules', case["mock_modules"]):
                    with patch('pathlib.Path.cwd', return_value=Path(self.test_dir)):
                        result = find_project_root()
                        self.assertEqual(result, case["expected"])

   

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
