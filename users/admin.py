from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, UserDevice, UserAlarm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'nickname', 'phone_number', 'register_date', 'personal_consent'
    )
    search_fields = ['id', 'nickname']


class UserDeviceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'fcm_token'
    )
    search_fields = ['user_id']


class UserAlarmAdmin(admin.ModelAdmin):
    list_display = (
        'register_user', 'target_user', 'content_id',
        'alarm_message', 'content_type', 'register_date'
    )
    search_fields = ['register_user', 'target_user', 'content_id', 'content_type']


admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(UserAlarm, UserAlarmAdmin)
