from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
import time

# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker = 'redis://192.168.1.111:6379/8')

@app.task
def send_register_active_email(to_email, username, token):
    subject = '天天生鲜欢迎信息(from centos)'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎成为天天生鲜注册会员<h1>请点击下面的链接激活您的账号<br/><a href="http://192.168.1.111/user/active/%s">请点击此处激活您的账户</a>' % (username, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)
    
