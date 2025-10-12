import requests
import json
from time import perf_counter
from typing import Optional, Dict, Any
import logging

class Log:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

# 时间装饰器工具类
def timeit(start_time: float) -> float:
    """
    :param start_time: 开始时间
    """
    elapsed_time = perf_counter() - start_time

    def decorator(func):
        def wrapper(*args, **kwargs):
            self.logger.info(f"开始执行测试用例...\n参数：{args}, {kwargs}")
            start_time = perf_counter()
            result = func(*args, **kwargs)
            run_time = perf_counter() - start_time

            self.logger.info(f"测试完成，耗时：{run_time:.6f}s。" +
                           f"\n返回值：>{json.dumps(result, indent=2)}\n" +
                           f"成功与否：{'成功' if result.get('success') else '失败'}")

            return result
        return wrapper
    return decorator

# 测试用例和设置类
@pytest.fixture(scope="session", params=["GET", "POST"],)
def test_api() -> tuple[str, Any]:
    """

    :return: 测试接口类型（如：'GET', 'POST' 等字符）
    """
    method = param.name
    return f"http://localhost:8000/api/v1/users"

@pytest.fixture()
def user_data() -> Dict:
    return {"userId": "123", "username": "testuser", "password": "testpass", "email": "testemail@example.com"}

try:
    # 打印测试开始信息
    print("\n开始执行用户管理接口测试...\n")

    @timeit()
    def test_get_user(userId: str):
        """

        :param userId: 用户ID字符串
        """
        response = requests.get(f"http://localhost:8000/api/v1/users/{userId}", timeout=10)

        # 分析响应
        try:
            response.raise_status()
        except exceptions.HTTPError as he:
            code = he.response.status
            reason = he.response.reason
            msg = f"HTTP错误：状态码 {code}, 原因: {reason}"

            self.logger.info(msg)
            raise ValueError

    @timeit()
    def test_create_user(**kwargs):
        """

        :param username: 用户名字符串
        :param password: 密码字符串
        :param email: 邮箱字符串
        """
        params = kwargs.copy()

        # 参数验证
        if not all([
            isinstance(params.get("username"), str),
            isinstance(params.get("password"), str),
            isinstance(params.get("email"), str)
        ]):
            params.pop("username", None)  # 确保只有有效键存在

        response = requests.post(
            test_api,
            json=params
        )

        try:
            response.raise_status()
        except exceptions.HTTPError as he:
            code = he.response.status
            reason = he.response.reason

            msg = f"HTTP错误：状态码 {code}, 原因: {reason}"

            self.logger.info(msg)
            raise ValueError

    # 其他测试函数同上

except Exception as e:
    error_msg = "测试过程中发生意外，请检查日志。"
    if isinstance(e, requests.exceptions.HTTPError):
        code = e.response.status
        reason = e.response.reason
        msg = f"HTTP错误：状态码 {code}, 原因: {reason}"
    else:
        msg = str(e)

    print(error_msg)