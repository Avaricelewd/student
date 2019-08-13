from django.db import models
from captcha.fields import  CaptchaField
# Create your models here.
# 可以使用django自带的AbstractUser表。 也可以继承再自己添加字段。
# 但内部代码不好修改，建议根据业务逻辑自己创建user表


class User(models.Model):
    name = models.CharField(verbose_name='用户名',max_length=20)
    email = models.CharField(verbose_name='邮箱', null=True,blank=True,max_length=100)
    password = models.CharField(verbose_name='密码',max_length=20)
    hash_password = models.CharField(verbose_name='哈希密码',max_length=256,null=True,blank=True)

    captcha = CaptchaField(label='验证码')
    # is_admin   join_time   last_login  等字段
