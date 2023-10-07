from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(verbose_name="별명", max_length=8, null=True)
    password = models.CharField(verbose_name="패스워드", max_length=32)
    phone_number = models.CharField(max_length=15, null=True)
    register_date = models.DateTimeField(auto_now_add=True, null=True)

    # profile_image = models.ImageField(
    #     "프로필 이미지", upload_to="users/profile", blank=True)
    # short_description = models.TextField("소개글", blank=True)
