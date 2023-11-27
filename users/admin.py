from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, UserDevice


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


admin.site.register(UserDevice, UserDeviceAdmin)
