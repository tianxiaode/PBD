import os
import pytest


def pytest_addoption(parser):
    # 环境参数配置
    parser.addoption(
        "--env",
        action="store",
        default=None,  # 设为 None 以便后续动态覆盖
        help="Set test environment (dev|staging|prod)"
    )
    
def pytest_configure(config):
    # 1. 动态设置默认环境
    if config.getoption("--env") is None:
        config.option.env = "staging" if os.getenv("CI") == "true" else "dev"
    
    # 2. 确保输出详细和捕获关闭（等效于 -sv）
    config.option.verbose = 1  # -v
    config.option.capture = "no"  # -s

@pytest.fixture
def env_config(request):
    """根据 env 参数返回环境配置"""
    env = request.config.getoption("--env")
    return {
        "dev": {"url": "http://localhost"},
        "staging": {"url": "https://staging.api.com"},
        "prod": {"url": "https://api.com"}
    }[env]

@pytest.fixture
def global_data():
    """所有测试文件均可使用的 fixture"""
    return {"key": "value"}