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
    url(r"^login/$", views.login_user),    # 登录
    url(r"^register/$", views.register),     # 注册
    url(r'code/$', views.create_code_img),    # 随机生成验证码
    url(r'logout/$', views.logout_user),      # 注销
    url(r'^index/$', views.index),      # 首页
    url(r'^business/manager/(\d*)$', views.business_manage),     # 企业信息管理
    url(r'^business/information/(\w+)/$', views.business_information),  # 企业详细信息查看
    url(r'^business/count/$', views.business_count),    # 企业统计
    url(r'^project/manager/(\d*)$', views.project_manage),     # 项目信息管理
    url(r'^project/information/(\w+)/$', views.project_information),  # 工程详细信息查看
    url(r'settings/$', views.settings),      # 个人资料设置
    url(r'^salary/check/(\d*)$', views.salary_check),     # 员工工资核对

]
