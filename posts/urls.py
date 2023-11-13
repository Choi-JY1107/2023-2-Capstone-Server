from django.urls import path
from posts.views import (CreatePostAPI, CreateMissingAPI, ListMissingAPI,
                         AlertMissingAPI)

urlpatterns = [
    path("create/", CreatePostAPI.as_view()),
    path("missing/create/", CreateMissingAPI.as_view()),
    path("missing/list/", ListMissingAPI.as_view()),
    path("missing/alert/", AlertMissingAPI.as_view()),
]