"""
    I l┃      ☃      ┃
            ┃ove animals.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
              ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^login/$", views.login),    # 登录
    url(r"^register/$", views.register),     # 注册
    url(r'code/$', views.create_code_img),    # 随机生成验证码
    url(r'^index/$', views.index),      # 首页
    url(r'^company/manager/$', views.company_manage),     # 企业信息管理
]