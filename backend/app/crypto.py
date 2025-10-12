import bcrypt, base64, os
from cryptography.fernet import Fernet

# ① 密码哈希
def hash_password(raw_pwd: str) -> str:
    return bcrypt.hashpw(raw_pwd.encode(), bcrypt.gensalt()).decode()

def verify_password(raw_pwd: str, hashed: str) -> bool:
    return bcrypt.checkpw(raw_pwd.encode(), hashed.encode())

# ② 验证码对称加密（key 放环境变量即可）
key = os.getenv("CODE_KEY", "bP0KJ4c1HN7u8v9y0A3T4w5X6y7Z8Q9R0S1t2U3v4W5x6Y7z8").encode()[:32]
fernet = Fernet(base64.urlsafe_b64encode(key))

def encrypt_code(code: str) -> str:
    return fernet.encrypt(code.encode()).decode()

def decrypt_code(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()