from django.contrib import admin
from .models import Animal, AnimalImage


class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'nickname', 'owner', 'main_img_id',
        'main_img', 'is_missing', 'register_date',
        'characteristic', 'missing_location',
    )
    search_fields = ['id', 'nickname']


class AnimalImageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'animal_id', 'image', 'register_date', 'is_learning'
    )
    search_fields = ['animal_id', 'is_learning', 'register_date']


admin.site.register(Animal, AnimalAdmin)
admin.site.register(AnimalImage, AnimalImageAdmin)
