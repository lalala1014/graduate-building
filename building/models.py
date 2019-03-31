from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# 企业类
class Business(models.Model):
    id = models.AutoField(primary_key=True)
    business_id = models.CharField(verbose_name="企业编号", max_length=22, unique=True)
    business_name = models.CharField(max_length=40, null=False, verbose_name="企业名称")
    manage_name = models.CharField(max_length=10, null=False, verbose_name="企业管理者")
    assess = models.CharField(max_length=10, default="优", verbose_name="企业信用评价")
    ensure_salary = models.FloatField(default=0, verbose_name="工资保障金余额")
    business_people_number = models.IntegerField(verbose_name="企业人数")


# 项目类
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    pro_id = models.CharField(verbose_name="项目编号", unique=True, max_length=22)
    project_name = models.CharField(max_length=50, null=False, verbose_name="项目名称")
    project_plan = models.CharField(max_length=10, verbose_name="工程进度", default="审批未开工")  # 工程进度有：审批未开工、在建、停工、竣工
    project_company = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name="建筑企业")
    project_unit = models.CharField(max_length=30, verbose_name="建筑单位")
    project_manager = models.CharField(max_length=20, verbose_name="项目负责人")


# 劳务公司
class Services(models.Model):
    id = models.AutoField(primary_key=True)
    ser_id = models.CharField(verbose_name="劳务公司号", unique=True, max_length=20)
    ser_name = models.CharField(verbose_name="劳务公司名称", max_length=40, null=False)
    ser_manager = models.CharField(verbose_name="劳务公司管理人", max_length=15)
    ser_number = models.IntegerField(verbose_name="劳务公司人数")


# 劳务人员类
class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.CharField(max_length=16, unique=True, verbose_name="员工编号")
    staff_name = models.CharField(max_length=10, null=False, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")
    native = models.CharField(verbose_name="籍贯", max_length=20)
    bank_num = models.CharField(max_length=30, verbose_name="银行卡号")
    company = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name="所属劳务公司")
    ID_card = models.CharField(verbose_name="身份证号", max_length=32)
    staff_position = models.CharField(max_length=10, verbose_name="工种", default="长期工")


# 考勤信息类
class Check(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, verbose_name="员工号")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="参与项目")
    time = models.DateTimeField(auto_now=True, verbose_name="考勤时间")


