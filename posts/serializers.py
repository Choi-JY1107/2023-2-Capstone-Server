from rest_framework import serializers

from users.models import User
from animal.models import AnimalImage
from .models import Post, PostImage, MissingImage


class FeedPostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    like_count = serializers.SerializerMethodField()
    content = serializers.CharField(max_length=1000)

    @staticmethod
    def get_like_count(obj):
        return obj.like_users.count()

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
    profile_number = serializers.IntegerField()

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
