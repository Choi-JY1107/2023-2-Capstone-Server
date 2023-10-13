from django.urls import path
from animal.views import (CreateAnimalAPI, CreateAnimalImageAPI,
                          DetailAnimalAPI, DetailAnimalImageAPI,
                          DeleteAnimalAPI, DeleteAnimalImageAPI,
                          ListAnimalAPI, ListAnimalImageAPI)


urlpatterns = [
    path("create/", CreateAnimalAPI.as_view()),
    path("image/create/", CreateAnimalImageAPI.as_view()),
    path("info/<int:pk>", DetailAnimalAPI.as_view()),
    path("image/info/<int:pk>", DetailAnimalImageAPI.as_view()),
    path("delete/<int:pk>", DeleteAnimalAPI.as_view()),
    path("image/delete/<int:pk>", DeleteAnimalImageAPI.as_view()),
    path("list/", ListAnimalAPI.as_view()),
    path("image/list/<int:pk>", ListAnimalImageAPI.as_view()),
]
