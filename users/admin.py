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
        'register_id', 'target_id', 'alarm_message',
        'type', 'register_date'
    )
    search_fields = ['register_id', 'target_id', 'type']


admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(UserAlarm, UserAlarmAdmin)
