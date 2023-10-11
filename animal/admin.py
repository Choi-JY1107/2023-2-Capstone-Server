from django.contrib import admin
from .models import Animal, AnimalImage


class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'nickname', 'owner_id', 'main_img_id',
        'main_img', 'is_missing', 'register_date'
    )
    search_fields = ['id', 'nickname']


class AnimalImageAdmin(admin.ModelAdmin):
    list_display = (
        'is_learning', 'register_date', 'image', 'animal_id'
    )
    search_fields = ['is_learning', 'register_date']


admin.site.register(Animal, AnimalAdmin)
admin.site.register(AnimalImage, AnimalImageAdmin)
