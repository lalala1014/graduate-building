from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# 企业类
class Business(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="企业号")
    business_name = models.CharField(max_length=40, null=False, verbose_name="企业名称")
    manage_name = models.CharField(max_length=10, null=False, verbose_name="企业管理者")
    assess = models.CharField(max_length=10, default="优", verbose_name="企业信用评价")
    ensure_salary = models.FloatField(default=0, verbose_name="工资保障金余额")


# 项目类
class Project(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="项目号")
    project_name = models.CharField(max_length=100, null=False, verbose_name="项目名称")
    project_plan = models.CharField(max_length=10,verbose_name="工程进度",default="审批未开工")  # 工程进度有：审批未开工、在建、停工、竣工
    project_company = models.ForeignKey(Business,on_delete=models.CASCADE,verbose_name="总包企业")


# 劳务人员类
class Staffs(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="员工号")
    staff_name = models.CharField(max_length=10, null=False, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")
    native = models.CharField(verbose_name="籍贯", max_length=20)
    bank_num = models.CharField(max_length=30, verbose_name="银行卡号")
    company = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name="所属劳务公司")


# 考勤信息类
class Check(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, verbose_name="员工号")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="参与项目")
    time = models.DateTimeField(auto_now=True, verbose_name="考勤时间")


