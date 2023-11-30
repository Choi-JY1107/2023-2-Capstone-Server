from django.urls import path
from posts.views import (CreatePostAPI, CreatePostImageAPI, CreateMissingAPI, ListMissingAPI,
                         ListFeedsAPI, LikeAPI)

urlpatterns = [
    path("create", CreatePostAPI.as_view()),
    path("image/create", CreatePostImageAPI.as_view()),
    path("feed", ListFeedsAPI.as_view()),
    path("missing/create", CreateMissingAPI.as_view()),
    path("missing/list", ListMissingAPI.as_view()),
    path("like", LikeAPI.as_view()),
]
