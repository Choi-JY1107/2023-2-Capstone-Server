from django.urls import path
from users.views import LoginAPI, LogoutAPI, SignupAPI, TestAPI

urlpatterns = [
    path("login/", LoginAPI.as_view()),
    path("logout/", LogoutAPI.as_view()),
    path("signup/", SignupAPI.as_view()),
    path("test/", TestAPI.as_view()),

]