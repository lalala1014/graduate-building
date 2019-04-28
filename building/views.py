from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import paginator
from building.models import *
from io import BytesIO
from . import utils
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

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


# 个人资料设置
@login_required
@csrf_exempt  # 跨站请求伪造
def settings(request):
    if request.method == "GET":
        return render(request, "settings.html", {"user": request.user})
    elif request.method == "POST":
        old_pwd = request.POST.get("old_pwd")    # 获取旧密码
        new_pwd = request.POST.get("new_pwd")    # 获取新密码
        alter_email = request.POST.get("alter_email")
        if old_pwd and new_pwd:
            if request.user.check_password(old_pwd):
                request.user.set_password(new_pwd)   # 修改密码
                request.user.save()
                is_alter = True
            else:
                is_alter = False
            return JsonResponse({"is_alter": is_alter})
        if alter_email:
            request.user.email = alter_email
            request.user.save()
            return JsonResponse({"is_alter": "修改成功！"})


# 首页
@login_required
def index(request):
    if request.method == "GET":
        a = connection.cursor()
        a.callproc(procname="select_business_count")
        c = a.fetchall()
        bus_count = c[0][0]
        a.callproc(procname="select_project_count")
        b = a.fetchall()
        pro_count = b[0][0]
        a.callproc(procname="select_staffs_count")
        d = a.fetchall()
        staffs_count = d[0][0]
        a.close()
        return render(request, "index.html", {"user": request.user, "business_count": bus_count,
                                              "project_count": pro_count, "staffs_count": staffs_count})
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
        return render(request, "business_manage.html", {"page": pages, "pag": pag, "user": request.user})
    elif request.method == "POST":
        business_name = request.POST.get("business_name")    # 企业名称
        business_id = request.POST.get("business_id")      # 企业编号
        corporate_representative = request.POST.get("corporate_representative")      # 法人代表
        assess = request.POST.get("assess")    # 企业评价
        search_dict = dict()   # 定义一个字典保存关键字
        if business_name:
            search_dict["business_name"] = business_name
        if business_id:
            search_dict["business_id"] = business_id
        if corporate_representative:
            search_dict["corporate_representative"] = corporate_representative
        if assess:
            search_dict["assess"] = assess
        search = Business.objects.filter(**search_dict).order_by("id")  # 使用字典匹配查询
        list_a = []
        for i in search:
            list_a.append(i.id)
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
    search_business = Business.objects.filter(id__in=request.session["search_business"]).order_by("id")
    if request.method == "GET":
        pag = paginator.Paginator(search_business, 1)
        pages = pag.page(pages)
        return render(request, "business_filter.html", {"page": pages, "pag": pag, "user": request.user})
    elif request.method == "POST":
        return render(request, "business_filter.html")


# 企业详细信息查看
@login_required
def business_information(request, business_id):
    if request.method == "GET":
        business = Business.objects.get(business_id=business_id)
        return render(request, "business_information.html", {"business": business, "user": request.user})
    elif request.method == "POST":
        return render(request, "business_information.html")


# TODO
# 企业统计
@login_required
def business_count(request):
    if request.method == "GET":
        return render(request, "business_count.html", {"user": request.user})
    elif request.method == "POST":
        return render(request, "business_count.html")


# TODO
# 企业评价
@login_required
@csrf_exempt  # 跨站请求伪造
def business_assess(request, page):
    business = Business.objects.all().order_by("id")  # 所有企业
    if page == "":
        pages = 1
    else:
        pages = int(page)
    if request.method == "GET":
        pag = paginator.Paginator(business, 2)
        pages = pag.page(pages)
        for i in pages:
            if i.pay_num >= 3:
                i.assess = "差"
                i.save()
            elif i.pay_num > 0:
                i.assess = "良"
                i.save()
            else:
                i.assess = "优"
                i.save()
        return render(request, "business_assess.html", {"page": pages, "pag": pag, "user": request.user})
    elif request.method == "POST":
        assess_id = request.POST.get("assess_id")    # 评价的企业id
        if assess_id:
            assess_business = Business.objects.get(id=assess_id)
            assess_business.is_business = "已吊销"
            assess_business.save()
            return JsonResponse({"is_business": "已吊销"})
        business_name = request.POST.get("business_name")  # 企业名称
        business_id = request.POST.get("business_id")  # 企业编号
        corporate_representative = request.POST.get("corporate_representative")  # 法人代表
        assess = request.POST.get("assess")  # 企业评价
        search_dict = dict()  # 定义一个字典保存关键字
        if business_name:
            search_dict["business_name"] = business_name
        if business_id:
            search_dict["business_id"] = business_id
        if corporate_representative:
            search_dict["corporate_representative"] = corporate_representative
        if assess:
            search_dict["assess"] = assess
        search = Business.objects.filter(**search_dict).order_by("id")  # 使用字典匹配查询
        list_a = []
        for i in search:
            list_a.append(i.id)
        request.session["assess_business"] = list_a
        if search.count() > 0:
            return JsonResponse({"is_filter": True})
        else:
            return JsonResponse({"is_filter": False})


# 企业评价查询结果
@login_required
@csrf_exempt  # 跨站请求伪造
def business_assess_filter(request, page):
    if page == "":
        pages = 1
    else:
        pages = int(page)
    search_business = Business.objects.filter(id__in=request.session["assess_business"]).order_by("id")
    if request.method == "GET":
        pag = paginator.Paginator(search_business, 1)
        pages = pag.page(pages)
        return render(request, "business_assess_filter.html", {"page": pages, "pag": pag, "user": request.user})
    elif request.method == "POST":
        assess_id = request.POST.get("assess_id")    # 评价的企业id
        assess_business = Business.objects.get(id=assess_id)
        assess_business.is_business = "已吊销"
        assess_business.save()
        return JsonResponse({"is_business": "已吊销"})


# ********************************************** 项 目 ******************************************************

# TODO
# 项目信息管理
@login_required
@csrf_exempt  # 跨站请求伪造
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
        return render(request, "project_manage.html", {"page": pages, "pag": pag, "user": request.user})
    elif request.method == "POST":
        project_name = request.POST.get("project_name")  # 项目名称
        project_id = request.POST.get("project_id")  # 项目编号
        project_unit = request.POST.get("project_unit")  # 建筑单位
        project_company = request.POST.get("project_company")    # 建筑企业
        project_plan = request.POST.get("plan")    # 工程进度
        project_region = request.POST.get("region")   # 所属区域
        print(project_name," 1",project_id," 2",project_unit,"3 ",project_company," 4",project_plan," 5 ",project_region)
        search_dict = dict()  # 定义一个字典保存关键字
        if project_name:
            search_dict["project_name"] = project_name
        if project_id:
            search_dict["pro_id"] = project_id
        if project_unit:
            search_dict["project_unit"] = project_unit
        if project_company:
            search_dict["project_company"] = project_company
        if project_plan:
            search_dict["project_plan"] = project_plan
        if project_region:
            search_dict["project_region"] = project_region
        search = Project.objects.filter(**search_dict).order_by("id")  # 使用字典匹配查询
        list_a = []
        for i in search:
            list_a.append(i.id)
        request.session["search_project"] = list_a
        if search.count() > 0:
            return JsonResponse({"is_filter": True})
        else:
            return JsonResponse({"is_filter": False})


# 项目详细信息查看
@login_required
def project_information(request, project_id):
    if request.method == "GET":
        project = Project.objects.get(pro_id=project_id)
        return render(request, "project_information.html", {"project": project, "user": request.user})
    elif request.method == "POST":
        return render(request, "project_information.html")


# 项目查询结果
@login_required
def project_filter(request, page):
    if page == "":
        pages = 1
    else:
        pages = int(page)
    search_business = Project.objects.filter(id__in=request.session["search_project"]).order_by("id")
    if request.method == "GET":
        pag = paginator.Paginator(search_business, 1)
        pages = pag.page(pages)
        return render(request, "project_filter.html", {"page": pages, "pag": pag, "user": request.user})
    elif request.method == "POST":
        return render(request, "project_filter.html")

# ********************************************** 劳 务 ******************************************************


# TODO
# 劳务人员考勤
@login_required
@csrf_exempt  # 跨站请求伪造
def staff_check(request, page):
    check_staffs = Check.objects.all().order_by("id")  # 所有企业
    if page == "":
        pages = 1
    else:
        pages = int(page)
    if request.method == "GET":
        pag = paginator.Paginator(check_staffs, 2)
        pages = pag.page(pages)
        return render(request, "staff_check.html", {"page": pages, "pag": pag, "user": request.user})
    elif request.method == "POST":
        staff_name = request.POST.get("staff_name")
        staff_id = request.POST.get("staff_id")
        staff_project = request.POST.get("staff_project")
        staff_company = request.POST.get("staff_company")
        project_unit = request.POST.get("project_unit")
        project_company = request.POST.get("project_company")
        search_dict = dict()  # 定义一个字典保存关键字
        if staff_name:
            search_dict["staff"] = Staffs.objects.filter(staff_name=staff_name)
        if staff_id:
            search_dict["staff"] = Staffs.objects.get(staff_id=staff_id)
        if staff_project:
            search_dict["project"] = Project.objects.get(project_name=staff_project)
        if staff_company:
            search_dict["staff"] = Staffs.objects.filter(staff_company=staff_company)
        if project_unit:
            search_dict["project"] = Project.objects.filter(project_unit=project_unit)
        if project_company:
            search_dict["project"] = Project.objects.filter(project_company=project_company)
        search = Project.objects.filter(**search_dict).order_by("id")  # 使用字典匹配查询
        list_a = []
        for i in search:
            list_a.append(i.id)
        request.session["search_staff"] = list_a
        if search.count() > 0:
            return JsonResponse({"is_filter": True})
        else:
            return JsonResponse({"is_filter": False})


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
            pag = paginator.Paginator(salary, 2)  # 每页的数据量, 实例化分页对象
            page_s = pag.page(pages)   # 该页的数据对象
        return render(request, "salary_check.html", {"page": page_s, "page_id": pages, "pag": pag, "user": request.user})
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
