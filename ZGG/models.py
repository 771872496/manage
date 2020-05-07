from django.contrib.auth.hashers import make_password
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True, verbose_name='用户ID')
    name = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=50, verbose_name='用户密码')
    zgg = models.ForeignKey('Authority', models.CASCADE, related_name='zgg')
    ltt = models.ForeignKey('Authority', models.CASCADE, related_name='ltt')
    state = models.CharField(max_length=20, verbose_name='用户状态', default='激活')

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'user'
        verbose_name_plural = '用户表'


class Authority(models.Model):
    a_name = models.CharField(max_length=300, default='权限')

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'authority'
        verbose_name_plural = '权限表'


class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True, verbose_name='工单ID')
    zc_type = models.CharField(max_length=100, verbose_name='资产状态')
    zc_number = models.CharField(max_length=200, verbose_name='资产编号')
    zc_name = models.CharField(max_length=200, verbose_name='资产名称')
    zc_site = models.CharField(max_length=200, verbose_name='资产地点')
    oa_id = models.CharField(max_length=200, verbose_name='OA请求ID')
    reception_bill = models.ImageField(upload_to='reception', null=True, blank=True, verbose_name='接收单')
    start_time = models.DateTimeField(verbose_name='录入时间', auto_now_add=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='操作人员')
    tag = models.CharField(max_length=100, verbose_name='标签')
    receive_name = models.CharField(max_length=100, verbose_name='领用人')
    other_bill = models.ImageField(upload_to='other', null=True, blank=True, verbose_name='对方申请单')
    state = models.CharField(max_length=100, verbose_name='状态', default='启用')
    execute_user = models.CharField(max_length=100, verbose_name='操作人员')
    pro1 = models.CharField(max_length=200, verbose_name='属性1')
    pro2 = models.CharField(max_length=200, verbose_name='属性2')
    pro3 = models.CharField(max_length=200, verbose_name='属性3', null=True, blank=True)

    def __str__(self):
        return self.bill_id

    class Meta:
        db_table = 'bill'
        verbose_name_plural = '工单表'
