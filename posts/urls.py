from django.urls import path
from posts.views import (CreatePostAPI, CreatePostImageAPI, CreateMissingAPI, ListMissingAPI, ListFeedsAPI, FindMissingAPI, LikeAPI)

urlpatterns = [
    path("create", CreatePostAPI.as_view()),
    path("image/create", CreatePostImageAPI.as_view()),
    path("feed", ListFeedsAPI.as_view()),
    path("missing/create", CreateMissingAPI.as_view()),
    path("missing/list", ListMissingAPI.as_view()),
    path("missing/find", FindMissingAPI.as_view()),
    path("like/<int:post_id>", LikeAPI.as_view()),
]
