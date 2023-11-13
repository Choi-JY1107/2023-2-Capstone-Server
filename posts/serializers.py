from rest_framework import serializers

from users.models import User
from .models import Post, PostImage, MissingImage


class FeedPostSerializer(serializers.Serializer):
    like_count = serializers.IntegerField()
    content = serializers.CharField(max_length=1000)
    main_img = serializers.CharField(max_length=255)
    register_id = serializers.CharField()
    register_date = serializers.DateTimeField()

    class Meta:
        model = Post
        fields = '__all__'


class FeedPostImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

    class Meta:
        model = PostImage
        fields = '__all__'


class MissingListSerializer(serializers.Serializer):
    register_id = serializers.CharField
    image = serializers.ImageField()
    register_date = serializers.DateTimeField()

    class Meta:
        model = MissingImage
        fields = '__all__'
