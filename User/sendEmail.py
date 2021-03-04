from __future__ import absolute_import
import smtplib
from email.mime.text import MIMEText
import random


def sendMail(email):
    from GraduationDesign.settings import MAIL_SENDER, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT
    code = random.randint(1111, 10000)
    content = f"""
        验证码为:{code}，该验证码用于修改密码,
        切勿向他人泄露，以防上当受骗。
    """
    # <a href="http://localhost:8000/user/reset_pwd/{email}/">点击链接确认</a>
    print(content)
    # 构建邮件格式
    message = MIMEText(content, "html", "utf-8")
    message["To"] = email
    message["From"] = MAIL_SENDER
    message["Subject"] = "密码修改"

    # 发送邮件
    smtp = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
    smtp.login(MAIL_SENDER, MAIL_PASSWORD)
    smtp.sendmail(MAIL_SENDER, [email], message.as_string())
    smtp.close()
    return code


if __name__ == '__main__':
    email = "2314348394@qq.com"
    code = sendMail(email)
    print(code)
