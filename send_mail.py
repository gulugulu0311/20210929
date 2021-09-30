import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '1079713055@qq.com'  # 发件人邮箱账号
my_pass = 'cexskgerbmhafdjj'  # 发件人邮箱授权码
my_user = '1079713055@qq.com'  # 收件人邮箱账号


def mail(title, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(['FromChristophr', my_sender])
    msg['TO'] = formataddr(['FK', my_user])
    msg['Subject'] = title

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com')
        server.login(my_sender, my_pass)
        server.set_debuglevel(1)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    mail('test', 'meow')
