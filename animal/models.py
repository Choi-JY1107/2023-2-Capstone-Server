from datetime import datetime
from django.db import models
import uuid

from users.models import User


class Animal(models.Model):
    nickname = models.CharField(verbose_name='반려동물 이름', max_length=8, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    characteristic = models.CharField(verbose_name='반려동물 특징', max_length=500, null=True, blank=True)
    main_img_id = models.IntegerField(default=-1)
    main_img = models.CharField(max_length=255, null=True, blank=True, default='')
    is_missing = models.BooleanField(default=False)
    missing_location = models.CharField(max_length=500, default='', null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Animal'

    def __str__(self):
        return str(self.id)

    def create_animal(data, user):
        animal = Animal.objects.create(
            nickname=data['nickname'],
            owner=user
        )

        return animal.id


class AnimalImage(models.Model):
    is_learning = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now_add=True, null=False)
    image = models.ImageField(verbose_name="동물 사진", upload_to="animal", blank=True)
    animal_id = models.ForeignKey(Animal, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'Animal_Image'

    def __str__(self):
        return str(self.image)

    def create_animal_image(image, animal_id):
        animal = Animal.objects.get(id=animal_id)
        image.name = str(datetime.today()) + str(uuid.uuid4()) + '.jpg'
        animal_image = AnimalImage.objects.create(
            image=image,
            animal_id=animal
        )

        if animal.main_img_id == -1:
            animal.main_img = str(animal_image)
            animal.main_img_id = animal_image.id
        animal.save()

        return animal_image
