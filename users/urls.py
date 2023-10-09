from django.urls import path
from users.views import LoginAPI, SignupAPI, TestAPI

urlpatterns = [
    path("login/", LoginAPI.as_view()),
    path("signup/", SignupAPI.as_view()),
    path("test/", TestAPI.as_view()),
]
