from django.db import models

# Create your models here.
class Student(models.Model):
    username = models.CharField(null=False, unique=True, max_length=15, help_text='用户名，用于登陆')
    # 这玩意儿就是学号吧
    password = models.CharField(null=False, max_length=32, )
