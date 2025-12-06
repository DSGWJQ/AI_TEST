# 测试配置文件
import pytest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def base_url():
    """后端 API 基础 URL"""
    return "http://localhost:8000"

@pytest.fixture
def api_headers():
    """通用 API 请求头"""
    return {
        "Content-Type": "application/json"
    }
