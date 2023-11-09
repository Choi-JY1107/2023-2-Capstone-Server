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
    image_id = models.ForeignKey(AnimalImage, on_delete=models.CASCADE, null=False)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Post_Image'

    def __str__(self):
        return str(self.id)

    def create_post_image(post_id, image_id):
        post = Post.objects.get(id=post_id)
        image = AnimalImage.objects.get(id=image_id)
        post_image = PostImage.objects.create(
            post=post,
            image=image
        )

        if post.main_img_id == -1:
            post.main_img = str(post_image)
            post.main_img_id = post_image.id
        post.save()


class PostLike(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Post_Like'

    def __str__(self):
        return str(self.id)
