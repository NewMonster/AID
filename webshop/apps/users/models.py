

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


class User(AbstractUser):
    """
    用户表
    """
    GENDER_ = ((0, '不详'), (1, '男'), (2, '女'))
    ch_name = models.CharField(max_length=50, verbose_name="中文姓名", default="匿名")
    gender = models.PositiveSmallIntegerField(choices=GENDER_, verbose_name="性别", default=0)
    update_pwd_time = models.DateTimeField(verbose_name='修改密码时间',
                                           default=timezone.now)
