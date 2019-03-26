# Generated by Django 2.1.7 on 2019-03-22 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='企业号')),
                ('business_name', models.CharField(max_length=40, verbose_name='企业名称')),
                ('manage_name', models.CharField(max_length=10, verbose_name='企业管理者')),
                ('assess', models.CharField(default='优', max_length=10, verbose_name='企业信用评价')),
                ('ensure_salary', models.FloatField(default=0, verbose_name='工资保障金余额')),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True, verbose_name='考勤时间')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='项目号')),
                ('project_name', models.CharField(max_length=100, verbose_name='项目名称')),
                ('project_plan', models.CharField(default='审批未开工', max_length=10, verbose_name='工程进度')),
                ('project_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='building.Business', verbose_name='总包企业')),
            ],
        ),
        migrations.CreateModel(
            name='Staffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='员工号')),
                ('staff_name', models.CharField(max_length=10, verbose_name='姓名')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('native', models.CharField(max_length=20, verbose_name='籍贯')),
                ('bank_num', models.CharField(max_length=30, verbose_name='银行卡号')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='building.Business', verbose_name='所属劳务公司')),
            ],
        ),
        migrations.AddField(
            model_name='check',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='building.Project', verbose_name='参与项目'),
        ),
        migrations.AddField(
            model_name='check',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='building.Staffs', verbose_name='员工号'),
        ),
    ]
