import requests
import json
import unittest

class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://localhost:8000'

    def test_get_root(self):
        try:
            response = requests.get(self.base_url + '/', timeout=10)
            response.raise_for_status()
            self.assertEqual(response.json()['code'], 200)
            self.assertEqual(response.json()['msg'], 'success')
            self.assertEqual(response.json()['data'], {'hello': 'world'})
        except requests.RequestException as e:
            self.fail(f"Request failed: {e}")

    def test_register(self):
        username = 'testuser'
        password = 'testpassword'
        try:
            response = requests.post(self.base_url + '/register', json={'username': username, 'password': password}, timeout=10)
            response.raise_for_status()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()['code'], 201)
            self.assertEqual(response.json()['msg'], '用户创建成功')
        except requests.RequestException as e:
            self.fail(f"Request failed: {e}")

    def test_register_missing_params(self):
        try:
            response = requests.post(self.base_url + '/register', json={'username': 'testuser'}, timeout=10)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()['code'], 400)
            self.assertEqual(response.json()['msg'], '缺少必填参数: username或password')
        except requests.RequestException as e:
            self.fail(f"Request failed: {e}")

    def test_register_duplicate_user(self):
        username = 'testuser'
        password = 'testpassword'
        try:
            response = requests.post(self.base_url + '/register', json={'username': username, 'password': password}, timeout=10)
            response.raise_for_status()
            response = requests.post(self.base_url + '/register', json={'username': username, 'password': password}, timeout=10)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()['code'], 400)
            self.assertEqual(response.json()['msg'], '用户已存在')
        except requests.RequestException as e:
            self.fail(f"Request failed: {e}")

    def test_login(self):
        username = 'testuser'
        password = 'testpassword'
        try:
            response = requests.post(self.base_url + '/register', json={'username': username, 'password': password}, timeout=10)
            response.raise_for_status()
            response = requests.post(self.base_url + '/login', json={'username': username, 'password': password}, timeout=10)
            response.raise_for_status()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['code'], 200)
            self.assertEqual(response.json()['msg'], 'success')
        except requests.RequestException as e:
            self.fail(f"Request failed: {e}")

    def test_login_wrong_credentials(self):
        username = 'testuser'
        password = 'testpassword'
        try:
            response = requests.post(self.base_url + '/register', json={'username': username, 'password': password}, timeout=10)
            response.raise_for_status()
            response = requests.post(self.base_url + '/login', json={'username': username, 'password': 'wrongpassword'}, timeout=10)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()['code'], 401)
            self.assertEqual(response.json()['msg'], '用户名或密码错误')
        except requests.RequestException as e:
            self.fail(f"Request failed: {e}")

    def test_send_code(self):
        email = 'test@example.com'
        try:
            response = requests.post(self.base_url + '/send-code', json={'email': email}, timeout=10)
            response.raise_for_status()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['code'], 200)
            self.assertEqual(response.json()['msg'], 'success')
        except requests.RequestException as e:
            self.fail(f"Request failed: {e}")

    def test_verify_code(self):
        email = 'test@example.com'
        try:
            response = requests.post(self.base_url + '/send-code', json={'email': email}, timeout=10)
            response.raise_for_status()
            response = requests.post(self.base_url + '/verify-code', json={'email': email, 'code': '123456'}, timeout=10)
            response.raise_for_status()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['code'], 200)
            self.assertEqual(response.json()['msg'], 'success')
        except requests.RequestException as e:
            self.fail(f"Request failed: {e}")

    def test_verify_code_wrong_code(self):
        email = 'test@example.com'
        try:
            response = requests.post(self.base_url + '/send-code', json={'email': email}, timeout=10)
            response.raise_for_status()
            response = requests.post(self.base_url + '/verify-code', json={'email': email, 'code': 'wrongcode'}, timeout=10)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()['code'], 400)
            self.assertEqual(response.json()['msg'], '验证码错误')
        except requests.RequestException as e:
            self.fail(f"Request failed: {e}")

if __name__ == '__main__':
    unittest.main()