from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from io import BytesIO
from . import utils
from django.views.decorators.csrf import csrf_exempt


# TODO
# 登录
@csrf_exempt  # 跨站请求伪造
def login(request):
    if request.method == "POST":
        username = request.POST.get("user")    # 获取用户名
        password = request.POST.get("password")    # 获取用户密码
        code = request.POST.get("code")   # 获取验证码
        manager = authenticate(username=username, password=password)   # 验证用户名和密码，返回用户对象
        print(manager)
        if manager:   # 判断用户对象是否存在
            if request.session['check_code'] == code:
                login(request, manager)   # 用户登录
                return JsonResponse({"isLogin": "登录成功"})
            else:
                return JsonResponse({"isLogin": "验证码错误"})
        else:
            return JsonResponse({"isLogin": "用户名或密码错误"})
    elif request.method == "GET":
        print("get请求")
        return render(request, "login2.html")


# TODO
# 注册
def register(request):
    username = request.POST.GET("username")     # 获取用户名
    password = request.POST.GET("password")     # 获取密码
    User.objects.create_user(username=username, password=password)    # 注册用户


# 在内存中开辟空间用以生成临时的图片
def create_code_img(request):
    f = BytesIO()
    img, code = utils.create_code()
    # 保存验证码信息到 session 中，方便下次表单提交时进行验证操作
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())
