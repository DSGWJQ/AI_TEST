import smtplib
import random
from email.message import EmailMessage

SMTP_SERVER = "smtp.163.com"   # 改为你自己的
SMTP_PORT   = 465
SMTP_USER   = "your_account@163.com"
SMTP_PASS   = "你的授权码"      # 不是登录密码！

def send_code(to_email: str, code: str):
    msg = EmailMessage()
    msg["Subject"] = "验证码"
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg.set_content(f"你的验证码是：{code} ，5分钟内有效。")

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)

def random_code() -> str:
    return str(random.randint(100000, 999999))