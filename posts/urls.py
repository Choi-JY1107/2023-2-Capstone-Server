from django.urls import path
from posts.views import CreatePostAPI, CreateMissingAPI, ListMissingAPI

urlpatterns = [
    path("create/", CreatePostAPI.as_view()),
    path("missing/create/", CreateMissingAPI.as_view()),
    path("missing/list/", ListMissingAPI.as_view()),
]