from django.urls import path
from animal.views import (CreateAnimalAPI, CreateAnimalImageAPI,
                          DetailAnimalAPI, DetailAnimalImageAPI,
                          ListAnimalAPI, ListAnimalImageAPI,
                          ListAllAnimalAPI)


urlpatterns = [
    path("create", CreateAnimalAPI.as_view()),
    path("<int:pk>", DetailAnimalAPI.as_view()),
    path("image/create", CreateAnimalImageAPI.as_view()),
    path("image/<int:pk>", DetailAnimalImageAPI.as_view()),
    path("list", ListAnimalAPI.as_view()),
    path("image/list/<int:pk>", ListAnimalImageAPI.as_view()),
    path("alllist", ListAllAnimalAPI.as_view()),
]
