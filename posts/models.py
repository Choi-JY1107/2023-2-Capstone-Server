from django.db import models

from users.models import User
from animal.models import AnimalImage


class Post(models.Model):
    like_count = models.PositiveIntegerField(default=0)
    content = models.CharField(max_length=1000, null=True)
    register_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Animal'

    def __str__(self):
        return str(self.id)


class PostImage(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    image_id = models.ForeignKey(AnimalImage, on_delete=models.CASCADE, null=False)
    register_data = models.DateTimeField(auto_now_add=True, null=False)


class PostLike(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    register_data = models.DateTimeField(auto_now_add=True, null=False)
