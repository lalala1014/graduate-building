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
    url(r'^business/manager/$', views.company_manage),     # 企业信息管理
    url(r'^project/manager/$', views.project_manage),     # 项目信息管理
    url(r'settings/$', views.settings),      # 个人资料设置
    url(r'^salary/check/$', views.salary_check),     # 员工工资核对
    url(r'^business/check/$', views.business_check),      # 企业审核
]
