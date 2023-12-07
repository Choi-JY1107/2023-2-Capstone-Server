from datetime import datetime
from django.db import models
import uuid

from users.models import User
from animal.models import Animal, AnimalImage


class Post(models.Model):
    content = models.CharField(max_length=1000, null=True)
    main_img_id = models.IntegerField(default=-1)
    main_img = models.CharField(max_length=255, null=True, blank=True, default='')
    register_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    register_date = models.DateTimeField(auto_now_add=True, null=False)
    like_users = models.ManyToManyField(User, related_name='like_users')

    class Meta:
        db_table = 'Post'

    def __str__(self):
        return str(self.id)

    def create_post(data, user):
        post = Post.objects.create(
            content=data['content'],
            register_id=user
        )

        return post.id


class PostImage(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    image = models.ForeignKey(AnimalImage, on_delete=models.CASCADE, null=False, related_name='animal_image')
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Post_Image'

    def __str__(self):
        return str(self.id)

    def create_post_image(animal_image_id, post_id):
        post = Post.objects.get(id=post_id)
        animal_image = AnimalImage.objects.get(id=animal_image_id)

        post_image = PostImage.objects.create(
            post_id=post,
            image=animal_image
        )

        if post.main_img_id == -1:
            post.main_img = str(animal_image)
            post.main_img_id = post_image.id
        post.save()

        return post_image


class MissingImage(models.Model):
    register_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    image = models.ImageField(verbose_name="실종 동물 사진", upload_to="missing", blank=True)
    possibility_animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    missing_location = models.CharField(max_length=500, default='', null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Missing_Image'

    def __str__(self):
        return str(self.id)

    def create_missing_image(image, user):
        print(str(datetime.today()) + str(uuid.uuid4()) + '.jpg')
        image.name = str(datetime.today()) + str(uuid.uuid4()) + '.jpg'
        missing_image = MissingImage.objects.create(
            image=image,
            register_id=user
        )

        return missing_image.id



class PostAlarm(models.Model):
    target_username = models.CharField(max_length=15, null=True)
    register_username = models.CharField(max_length=15, null=True)
    alarm_message = models.CharField(max_length=100, null=False)
    content_type = models.IntegerField(null=False, blank=False)
    content_id = models.IntegerField(null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Post_Alarm'

    def create_user_alarm(target_username, register_username, content_type, content_id):
        alarm_message = ""
        if content_type == 1:
            alarm_message = "당신의 실종 동물에 대한 제보가 들어왔습니다."
        if content_type == 2:
            alarm_message = "누군가가 동물을 잃어버렸습니다."
        if content_type == 3:
            alarm_message = "당신의 게시글에 발자국을 남겼습니다."

        post_alarm = PostAlarm.objects.create(
            target_username=target_username,
            register_username=register_username,
            alarm_message=alarm_message,
            content_type=content_type,
            content_id=content_id,
        )

        return post_alarm

    def __str__(self):
        return str(self.id)
