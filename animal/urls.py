from django.urls import path
from animal.views import CreateAnimalAPI

urlpatterns = [
    path("create/", CreateAnimalAPI.as_view()),
    # path("(?P<pk>\d+/$", )
]
