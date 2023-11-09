from django.urls import path
from posts.views import CreatePostAPI, CreateMissingAPI

urlpatterns = [
    path("create/", CreatePostAPI.as_view()),
    path("missing/create/", CreateMissingAPI.as_view()),
]