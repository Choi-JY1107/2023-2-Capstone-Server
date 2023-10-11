from django.db import models
from django.contrib.auth.models import AbstractUser

from users.models import User


class Animal(models.Model):
    nickname = models.CharField(verbose_name='반려동물 이름', max_length=8, null=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    main_img_id = models.IntegerField(default=-1)
    main_img = models.CharField(max_length=255, null=True, blank=True)
    is_missing = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Animal'


class AnimalImage(models.Model):
    is_learning = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now_add=True, null=False)
    image = models.ImageField(verbose_name="동물 사진", upload_to="animal", blank=True)
    animal_id = models.ForeignKey(Animal, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'Animal_Image'
