from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import paginator
from building.models import *
from io import BytesIO
from . import utils
from django.views.decorators.csrf import csrf_exempt


# ********************************************** 账 户 ******************************************************

# 登录
@csrf_exempt  # 跨站请求伪造
def login_user(request):
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
        try:
            User.objects.get(username=username)
            return JsonResponse({"isRegister": "用户已存在"})
        except Exception as e:
            User.objects.create_user(username=username, password=password, email=email)  # 注册用户
            return JsonResponse({"isRegister": "注册成功"})


# 注销
@login_required
def logout_user(request):
    logout(request)
    return redirect("/building/login/")


# TODO
# 个人资料设置
@login_required
def settings(request):
    if request.method == "GET":
        return render(request, "settings.html")
    elif request.method == "POST":
        return render(request, "settings.html")


# TODO
# 首页
@login_required
def index(request):
    if request.method == "GET":
        return render(request, "index.html", {"user": request.user})
    elif request.method == "POST":
        return render(request, "index.html")


# ********************************************** 企 业 ******************************************************

# TODO
# 企业信息管理
@login_required
@csrf_exempt  # 跨站请求伪造
def business_manage(request, page):
    business = Business.objects.all().order_by("id")  # 所有企业
    if page == "":
        pages = 1
    else:
        pages = int(page)
    if request.method == "GET":
        pag = paginator.Paginator(business, 1)
        pages = pag.page(pages)
        return render(request, "business_manage.html", {"page": pages, "pag": pag})
    elif request.method == "POST":
        business_name = request.POST.get("business_name")    # 企业名称
        business_id = request.POST.get("business_id")      # 企业编号
        corporate_representative = request.POST.get("corporate_representative")      # 法人代表
        search_dict = dict()   # 定义一个字典保存关键字
        if business_name:
            search_dict["business_name"] = business_name
        if business_id:
            search_dict["business_id"] = business_id
        if corporate_representative:
            search_dict["corporate_representative"] = corporate_representative
        search = Business.objects.filter(**search_dict).order_by("id")  # 使用字典匹配查询
        list_a = []
        for i in search:
            list_a.append(i.id)
            print(type(i.id),i.id)
        request.session["search_business"] = list_a
        if search.count() > 0:
            return JsonResponse({"is_filter": True})
        else:
            return JsonResponse({"is_filter": False})


# 企业查询结果
@login_required
def business_filter(request, page):
    if page == "":
        pages = 1
    else:
        pages = int(page)
    for i in request.session["search_business"]:
        search_business = Business.objects.filter(id=str(i)).order_by("id")
#####################此处有错误
        # print(search_business)
    if request.method == "GET":
        # return render(request, "business_filter.html")
        pag = paginator.Paginator(search_business, 1)
        pages = pag.page(pages)
        print(pages.number)
        return render(request, "business_filter.html", {"page": pages, "pag": pag})
    elif request.method == "POST":
        return render(request, "business_filter.html")


# 企业详细信息查看
@login_required
def business_information(request, business_id):
    if request.method == "GET":
        business = Business.objects.get(business_id=business_id)
        return render(request, "business_information.html", {"business": business})
    elif request.method == "POST":
        return render(request, "business_information.html")


# TODO
# 企业统计
@login_required
def business_count(request):
    if request.method == "GET":
        return render(request, "business_count.html")
    elif request.method == "POST":
        return render(request, "business_count.html")


# ********************************************** 项 目 ******************************************************

# TODO
# 项目信息管理
@login_required
def project_manage(request, page):
    if request.method == "GET":
        project = Project.objects.all().order_by("id")   # 所有项目
        if page == "":
            pages = 1
        else:
            pages = int(page)
        if request.method == "GET":
            pag = paginator.Paginator(project, 1)     # 每页的数据量
            pages = pag.page(pages)
        return render(request, "project_manage.html", {"page": pages, "pag": pag})
    elif request.method == "POST":
        return render(request, "project_manage.html")


# TODO
# 项目详细信息查看
@login_required
def project_information(request, project_id):
    if request.method == "GET":
        project = Project.objects.get(pro_id=project_id)
        return render(request, "project_information.html", {"project": project})
    elif request.method == "POST":
        return render(request, "project_information.html")


# ********************************************** 工 资 ******************************************************


# 工资核对
@login_required
@csrf_exempt  # 跨站请求伪造
def salary_check(request, page):
    if request.method == "GET":
        salary = Salary.objects.all().order_by("id")  # 所有工资详情排序
        if page == "":
            pages = 1
        else:
            pages = int(page)
        if request.method == "GET":
            pag = paginator.Paginator(salary, 1)  # 每页的数据量, 实例化分页对象
            page_s = pag.page(pages)   # 该页的数据对象
        return render(request, "salary_check.html", {"page": page_s, "page_id": pages, "pag": pag})
    elif request.method == "POST":
        check_id = request.POST.get("check_id")
        check_peo = Salary.objects.get(id=check_id)
        check_peo.is_manager = "已核对"
        check_peo.save()
        return JsonResponse({"is_check": "已核对"})


# 在内存中开辟空间用以生成临时的图片
def create_code_img(request):
    f = BytesIO()
    img, code = utils.create_code()
    # 保存验证码信息到 session 中，方便下次表单提交时进行验证操作
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())
