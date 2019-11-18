from django.urls import re_path 
from . import views
from .views import RegisterView, ActivateView, LoginView

urlpatterns = [
    # re_path(r'register$', views.register, name='register'), # 注册
    # re_path(r'register_handle$', views.register_handle, name='register_handle'), # 注册处理
    re_path(r'register$', RegisterView.as_view(), name='register'),
    re_path(r'^active/(?P<token>.*)$', ActivateView.as_view(), name='activate'),
    re_path(r'login$', LoginView.as_view(), name='login'),
    
]
