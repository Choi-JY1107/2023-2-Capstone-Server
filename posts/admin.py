from django.contrib import admin
from .models import Post, PostImage, PostLike, MissingImage


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'content', 'register_id', 'register_date', 'like_count'
    )
    search_fields = ['content', 'register_id']


class PostImageAdmin(admin.ModelAdmin):
    list_display = (
        'post_id', 'image', 'register_date'
    )
    search_fields = ['post_id', 'image_id']


class PostLikeAdmin(admin.ModelAdmin):
    list_display = (
        'post_id', 'user_id', 'register_date'
    )
    search_fields = ['post_id', 'user_id']


class MissingImageAdmin(admin.ModelAdmin):
    list_display = (
        'register_id', 'image', 'register_date'
    )
    search_fields = ['register_id', 'image']


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(MissingImage, MissingImageAdmin)
