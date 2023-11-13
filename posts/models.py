from datetime import datetime
from django.db import models
import uuid

from users.models import User
from animal.models import AnimalImage


class Post(models.Model):
    like_count = models.PositiveIntegerField(default=0)
    content = models.CharField(max_length=1000, null=True)
    main_img_id = models.IntegerField(default=-1)
    main_img = models.CharField(max_length=255, null=True, blank=True, default='')
    register_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

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
    image = models.ImageField(verbose_name="post 사진", upload_to="posts", blank=True)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Post_Image'

    def __str__(self):
        return str(self.id)

    def create_post_image(image, post_id):
        post = Post.objects.get(id=post_id)

        image.name = str(datetime.today()) + str(uuid.uuid4()) + '.jpg'
        post_image = PostImage.objects.create(
            image=image,
            post_id=post
        )

        if post.main_img_id == -1:
            post.main_img = str(image.name)
            post.main_img_id = post_image.id
        post.save()

        return post_image


class PostLike(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Post_Like'

    def __str__(self):
        return str(self.id)


class MissingImage(models.Model):
    register_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    image = models.ImageField(verbose_name="실종 동물 사진", upload_to="missing", blank=True)
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
