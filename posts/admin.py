from django.contrib import admin
from .models import Post, PostImage, PostLike


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'content', 'register_id', 'register_date', 'like_count'
    )
    search_fields = ['content', 'register_id']


class PostImageAdmin(admin.ModelAdmin):
    list_display = (
        'post_id', 'image_id', 'register_date'
    )
    search_fields = ['post_id', 'image_id']


class PostLikeAdmin(admin.ModelAdmin):
    list_display = (
        'post_id', 'user_id', 'register_date'
    )
    search_fields = ['post_id', 'user_id']


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(PostLike, PostLikeAdmin)
