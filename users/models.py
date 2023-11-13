from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(verbose_name="별명", max_length=8, null=False, unique=True)
    password = models.CharField(verbose_name="패스워드", max_length=20)
    phone_number = models.CharField(max_length=15, null=True)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return str(self.id)

class UserDevice(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="", null=True
    )
    fcm_token = models.CharField("FCM Token", blank=True, max_length=500, null=True)

    class Meta:
        db_table = 'User_Device'