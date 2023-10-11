from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'nickname', 'phone_number', 'register_date'
    )
    search_fields = ['id', 'nickname']