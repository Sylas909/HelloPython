from django.urls import re_path 
from . import views

urlpatterns = [
    re_path(r'register$', views.register, name='register'), # 注册
    re_path(r'register_handle$', views.register_handle, name='register_handle'), # 注册处理
]
