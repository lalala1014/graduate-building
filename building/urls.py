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
    url(r"^login/$", views.login),
    url(r'code/$', views.create_code_img)
]