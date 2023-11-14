from django.urls import path
from posts.views import (CreatePostAPI, CreatePostImageAPI,CreateMissingAPI, ListMissingAPI,
                         AlertMissingAPI, ListFeedsAPI)

urlpatterns = [
    path("create/", CreatePostAPI.as_view()),
    path("images/create/", CreatePostImageAPI.as_view()),
    path("feeds/", ListFeedsAPI.as_view()),
    path("missing/create/", CreateMissingAPI.as_view()),
    path("missing/list/", ListMissingAPI.as_view()),
    path("missing/alert/", AlertMissingAPI.as_view()),
]