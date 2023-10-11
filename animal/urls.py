from django.urls import path
from animal.views import CreateAnimalAPI

urlpatterns = [
    path("test/", CreateAnimalAPI.as_view()),
]
