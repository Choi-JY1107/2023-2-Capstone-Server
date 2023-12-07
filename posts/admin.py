from django.contrib import admin
from .models import Post, PostImage, MissingImage, PostAlarm


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'content', 'register_id', 'register_date'
    )
    search_fields = ['content', 'register_id']


class PostImageAdmin(admin.ModelAdmin):
    list_display = (
        'post_id', 'image', 'register_date'
    )
    search_fields = ['post_id', 'image_id']


class MissingImageAdmin(admin.ModelAdmin):
    list_display = (
        'register_id', 'image', 'register_date', 'phone_number', 'missing_location'
    )
    search_fields = ['register_id', 'image', 'phone_number', 'missing_location']

class PostAlarmAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'target_username', 'register_username', 'alarm_message',
        'content_type', 'content_id', 'register_date',
    )
    search_fields = ['id', 'target_username', 'register_username', 'alarm_message',
                     'content_type', 'content_id']


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(MissingImage, MissingImageAdmin)
admin.site.register(PostAlarm, PostAlarmAdmin)
