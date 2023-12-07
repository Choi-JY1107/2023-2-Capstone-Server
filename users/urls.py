from django.urls import path
from users.views import LoginAPI, SignupAPI, UserInfoAPI, UserAlarmListAPI

urlpatterns = [
    path("login", LoginAPI.as_view()),
    path("signup", SignupAPI.as_view()),
    path("info", UserInfoAPI.as_view()),
    path("alarm/list", UserAlarmListAPI.as_view()),
]
