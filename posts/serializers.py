from rest_framework import serializers

from .models import MissingImage


class MissingListSerializer(serializers.Serializer):
    register_id = serializers.CharField
    image = serializers.ImageField()
    register_date = serializers.DateTimeField()

    class Meta:
        model = MissingImage
        fields = '__all__'
