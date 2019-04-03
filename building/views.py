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
        if manager:   # 判断用户对象是否存在
            if request.session['check_code'] == code:
                login(request, manager)   # 用户登录
                return JsonResponse({"isLogin": True})
            else:
                return JsonResponse({"isLogin": "验证码错误"})
        else:
            return JsonResponse({"isLogin": "用户名或密码错误"})
    elif request.method == "GET":
        return render(request, "login.html")


# TODO
# 注册
@csrf_exempt  # 跨站请求伪造
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST.get("user")     # 获取用户名
        password = request.POST.get("password")     # 获取密码
        email = request.POST.get("email")      # 获取电子邮箱
        users = User.objects.all()      # 所有的用户
        for i in users:
            if str(i) == username:
                print("用户已存在")
            else:
                User.objects.create_user(username=username, password=password, email=email)  # 注册用户

        return JsonResponse({"isRegister": "注册成功"})


# TODO
# 首页
def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    elif request.method == "POST":
        return render(request, "index.html")


# TODO
# 企业信息管理
def company_manage(request):
    if request.method == "GET":
        return render(request, "company_information.html")
    elif request.method == "POST":
        return render(request, "company_information.html")


# TODO
# 项目信息管理
def project_manage(request):
    if request.method == "GET":
        return render(request, "project_information.html")
    elif request.method == "POST":
        return render(request, "project_information.html")


# TODO
# 个人资料设置
def settings(request):
    if request.method == "GET":
        return render(request, "settings.html")
    elif request.method == "POST":
        return render(request, "settings.html")


# TODO
# 工资核对
def salary_check(request):
    if request.method == "GET":
        return render(request, "salary_check.html")
    elif request.method == "POST":
        return render(request, "salary_check.html")


# TODO
# 企业审核
def business_check(request):
    if request.method == "GET":
        return render(request, "business_check.html")
    elif request.method == "POST":
        return render(request, "business_check.html")


# 在内存中开辟空间用以生成临时的图片
def create_code_img(request):
    f = BytesIO()
    img, code = utils.create_code()
    # 保存验证码信息到 session 中，方便下次表单提交时进行验证操作
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())
