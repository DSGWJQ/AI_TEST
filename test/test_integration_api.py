"""
后端 API 集成测试
测试后端 API 接口功能
"""
import pytest
import requests
import json
import time


class TestRootAPI:
    """测试根路径 API"""

    def test_root_endpoint(self, base_url, api_headers):
        """测试根路径返回正确响应"""
        response = requests.get(f"{base_url}/", headers=api_headers, timeout=10)
        assert response.status_code == 200

        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "success"
        assert data["data"]["hello"] == "world"

    def test_root_endpoint_response_format(self, base_url, api_headers):
        """测试根路径响应格式"""
        response = requests.get(f"{base_url}/", headers=api_headers, timeout=10)
        data = response.json()

        # 验证响应包含必需字段
        assert "code" in data
        assert "msg" in data
        assert "data" in data


class TestRunCodeAPI:
    """测试代码执行 API"""

    def test_run_simple_python_code(self, base_url, api_headers):
        """测试执行简单 Python 代码"""
        payload = {
            "code": "print('Hello, World!')",
            "runner": "python",
            "timeout": 30
        }
        response = requests.post(
            f"{base_url}/run-code",
            headers=api_headers,
            json=payload,
            timeout=60
        )
        assert response.status_code == 200

        data = response.json()
        assert data["code"] == 200
        assert "Hello, World!" in data["data"]["stdout"]

    def test_run_code_with_calculation(self, base_url, api_headers):
        """测试执行包含计算的代码"""
        payload = {
            "code": "result = 1 + 2 + 3\nprint(f'Result: {result}')",
            "runner": "python",
            "timeout": 30
        }
        response = requests.post(
            f"{base_url}/run-code",
            headers=api_headers,
            json=payload,
            timeout=60
        )
        assert response.status_code == 200

        data = response.json()
        assert data["code"] == 200
        assert "Result: 6" in data["data"]["stdout"]

    def test_run_empty_code(self, base_url, api_headers):
        """测试执行空代码"""
        payload = {
            "code": "",
            "runner": "python",
            "timeout": 30
        }
        response = requests.post(
            f"{base_url}/run-code",
            headers=api_headers,
            json=payload,
            timeout=60
        )
        assert response.status_code == 200

        data = response.json()
        # 空代码应该返回错误
        assert data["code"] != 200

    def test_run_code_syntax_error(self, base_url, api_headers):
        """测试执行语法错误的代码"""
        payload = {
            "code": "def test( :",
            "runner": "python",
            "timeout": 30
        }
        response = requests.post(
            f"{base_url}/run-code",
            headers=api_headers,
            json=payload,
            timeout=60
        )
        assert response.status_code == 200

        data = response.json()
        # 语法错误应该返回错误码
        assert data["code"] == 400
        assert "语法错误" in data["msg"]

    def test_run_pytest_code(self, base_url, api_headers):
        """测试执行 pytest 测试代码"""
        payload = {
            "code": """
import pytest

def test_addition():
    assert 1 + 1 == 2

def test_subtraction():
    assert 5 - 3 == 2
""",
            "runner": "pytest",
            "timeout": 60
        }
        response = requests.post(
            f"{base_url}/run-code",
            headers=api_headers,
            json=payload,
            timeout=90
        )
        assert response.status_code == 200

        data = response.json()
        # pytest 应该成功执行
        assert data["data"]["runner"] == "pytest"

    def test_run_code_with_invalid_runner(self, base_url, api_headers):
        """测试使用无效的运行器"""
        payload = {
            "code": "print('test')",
            "runner": "invalid_runner",
            "timeout": 30
        }
        response = requests.post(
            f"{base_url}/run-code",
            headers=api_headers,
            json=payload,
            timeout=60
        )
        assert response.status_code == 200

        data = response.json()
        # 无效运行器应该返回错误
        assert data["code"] != 200

    def test_run_code_response_structure(self, base_url, api_headers):
        """测试代码执行响应结构"""
        payload = {
            "code": "print('test')",
            "runner": "python",
            "timeout": 30
        }
        response = requests.post(
            f"{base_url}/run-code",
            headers=api_headers,
            json=payload,
            timeout=60
        )
        data = response.json()

        # 验证响应数据结构
        if data["code"] == 200:
            assert "stdout" in data["data"]
            assert "stderr" in data["data"]
            assert "exit_code" in data["data"]
            assert "status" in data["data"]


class TestAIChatAPI:
    """测试 AI 聊天 API"""

    def test_ai_chat_missing_api_key(self, base_url, api_headers):
        """测试缺少 API Key 的情况"""
        payload = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}]
        }
        response = requests.post(
            f"{base_url}/ai/chat",
            headers=api_headers,
            json=payload,
            timeout=30
        )
        assert response.status_code == 400

        data = response.json()
        assert "error" in data

    def test_ai_chat_invalid_api_key_format(self, base_url, api_headers):
        """测试无效的 API Key 格式"""
        payload = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "api_key": "invalid-key"
        }
        response = requests.post(
            f"{base_url}/ai/chat",
            headers=api_headers,
            json=payload,
            timeout=30
        )
        assert response.status_code == 400

        data = response.json()
        assert "error" in data
        assert "格式错误" in data["error"]

    def test_ai_chat_missing_model(self, base_url, api_headers):
        """测试缺少模型参数"""
        payload = {
            "messages": [{"role": "user", "content": "Hello"}],
            "api_key": "sk-or-v1-test"
        }
        response = requests.post(
            f"{base_url}/ai/chat",
            headers=api_headers,
            json=payload,
            timeout=30
        )
        assert response.status_code == 400

        data = response.json()
        assert "error" in data

    def test_ai_chat_missing_messages(self, base_url, api_headers):
        """测试缺少消息参数"""
        payload = {
            "model": "test-model",
            "api_key": "sk-or-v1-test"
        }
        response = requests.post(
            f"{base_url}/ai/chat",
            headers=api_headers,
            json=payload,
            timeout=30
        )
        assert response.status_code == 400

        data = response.json()
        assert "error" in data


class TestAPIErrorHandling:
    """测试 API 错误处理"""

    def test_invalid_endpoint(self, base_url, api_headers):
        """测试访问不存在的端点"""
        response = requests.get(
            f"{base_url}/invalid-endpoint",
            headers=api_headers,
            timeout=10
        )
        # FastAPI 对不存在的路由返回 404
        assert response.status_code == 404

    def test_invalid_method(self, base_url, api_headers):
        """测试使用错误的 HTTP 方法"""
        response = requests.get(
            f"{base_url}/run-code",
            headers=api_headers,
            timeout=10
        )
        # GET 方法应该返回 405 Method Not Allowed
        assert response.status_code == 405

    def test_invalid_json_body(self, base_url, api_headers):
        """测试发送无效的 JSON 请求体"""
        response = requests.post(
            f"{base_url}/run-code",
            headers=api_headers,
            data="invalid json",
            timeout=10
        )
        # 无效 JSON 应该返回 422 或 400
        assert response.status_code in [400, 422]
