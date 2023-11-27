from rest_framework import serializers

from users.models import User
from animal.models import AnimalImage
from .models import Post, PostImage, MissingImage


class FeedPostSerializer(serializers.Serializer):
    like_count = serializers.IntegerField()
    content = serializers.CharField(max_length=1000)

    class Meta:
        model = Post
        fields = '__all__'


class FeedPostImageSerializer(serializers.Serializer):
    image = serializers.ImageField(source='image.image')

    class Meta:
        model = AnimalImage
        fields = '__all__'


class FeedWriteSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=8)
    profile_image = serializers.ImageField()

    class Meta:
        model = User
        fields = '__all__'


class FeedSerializer(serializers.Serializer):
    post = serializers.ListField(child=serializers.CharField())
    images = serializers.ListField()
    user = serializers.ListField()


class MissingListSerializer(serializers.Serializer):
    register_id = serializers.CharField
    image = serializers.ImageField()
    register_date = serializers.DateTimeField()

    class Meta:
        model = MissingImage
        fields = '__all__'
