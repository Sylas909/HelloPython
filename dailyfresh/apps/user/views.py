from django.shortcuts import render, redirect
from django.http import HttpResponse
import re
from django.urls import reverse
from .models import User
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from celery_tasks.tasks import send_register_active_email

# Create your views here.
def register(request):
    '''显示注册页面'''
    return render(request, 'register.html')

def register_handle(request):
    '''进行注册处理'''
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')

    if not all([username, password, email]):
        # 数据不完整
        return render(request, 'register.html', {'errmsg':'数据不完整'})

    # 校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg':'邮箱格式不正确'})

    if allow != 'on':
        return render(request, 'register.html', {'errmsg': '请同意协议'})

    # 进行业务处理: 进行用户注册
    user = User.objects.create_user(username, email, password)

    # 返回应答, 跳转到首页
    return redirect(reverse('goods:index'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        '''进行注册处理'''
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg':'数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg':'邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 进行业务处理: 进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发邮件
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # 加密
        token = token.decode()  # utf-8解码

        send_register_active_email.delay(email, username, token)

        # 返回应答, 跳转到首页
        return redirect(reverse('goods:index'))


class ActivateView(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)        
        try:
           # 解密
           info = serializer.loads(token)
           # 获取用户id
           user_id = info['confirm']
           current_user = User.objects.get(pk=user_id)
           current_user.is_active = 1
           current_user.save()
           return redirect(reverse('user:login'))

        except SignatureExpired as e:
            return HttpResponse('激活链接已经过期')
            

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

