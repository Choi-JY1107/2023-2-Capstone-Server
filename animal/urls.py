from django.urls import path
from animal.views import (CreateAnimalAPI, CreateAnimalImageAPI,
                          DetailAnimalAPI, ChangeAnimalImageAPI,
                          ListAnimalAPI, ListAnimalImageAPI,
                          ListMyAnimalImageAPI,
                          ListAllAnimalAPI, AlertMissingAPI, FoundMyPetAPI)


urlpatterns = [
    path("create", CreateAnimalAPI.as_view()),
    path("<int:pk>", DetailAnimalAPI.as_view()),
    path("image/create", CreateAnimalImageAPI.as_view()),
    path("image/<int:pk>", ChangeAnimalImageAPI.as_view()),
    path("list", ListAnimalAPI.as_view()),
    path("image/list/<int:pk>", ListAnimalImageAPI.as_view()),
    path("image/mylist", ListMyAnimalImageAPI.as_view()),
    path("alllist", ListAllAnimalAPI.as_view()),
    path("alert", AlertMissingAPI.as_view()),
    path("found/<int:pk>", FoundMyPetAPI.as_view()),
]
