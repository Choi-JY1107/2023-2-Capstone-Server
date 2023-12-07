from django.urls import path
from posts.views import (CreatePostAPI, CreatePostImageAPI, CreateMissingAPI, ListMissingAPI,
                         ListFeedsAPI, FindMissingAPI, LikeAPI, ListAlarmAPI, DetailAlarmAPI)

urlpatterns = [
    path("create", CreatePostAPI.as_view()),
    path("image/create", CreatePostImageAPI.as_view()),
    path("feed", ListFeedsAPI.as_view()),
    path("missing/create", CreateMissingAPI.as_view()),
    path("missing/list", ListMissingAPI.as_view()),
    path("missing/find", FindMissingAPI.as_view()),
    path("like/<int:post_id>", LikeAPI.as_view()),
    path("alarm/list", ListAlarmAPI.as_view()),
    path("alarm/<int:pk>", DetailAlarmAPI.as_view()),
]
