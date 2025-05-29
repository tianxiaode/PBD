import pytest
import sys
from pathlib import Path

# 假设结构：workspace_root/packages/pkg1/src/, workspace_root/tests/
WORKSPACE_DIR = Path(__file__).parent.parent
FRAMEWORK_DIR = WORKSPACE_DIR / "framework"

# 添加所有子包目录到路径
sys.path.insert(0, str(WORKSPACE_DIR))
for pkg_path in FRAMEWORK_DIR.glob("*/src"):  # 遍历每个包的 src/ 目录
    if str(pkg_path) not in sys.path:
        sys.path.insert(0, str(pkg_path))

@pytest.fixture
def local_data(global_data):  # 可以依赖上级的 fixture
    """仅对 tests/ 下的测试生效"""
    return global_data