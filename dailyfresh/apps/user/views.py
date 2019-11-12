from django.shortcuts import render
import re
from django.urls import reverse

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

