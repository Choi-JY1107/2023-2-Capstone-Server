from rest_framework import serializers

from .models import Animal, AnimalImage


class AnimalInfoSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=8)
    owner_id = serializers.CharField()
    main_img_id = serializers.IntegerField()
    main_img = serializers.CharField(max_length=255)
    is_missing = serializers.BooleanField()
    register_date = serializers.DateTimeField()

    class Meta:
        model = Animal
        fields = '__all__'


class AnimalImageSerializer(serializers.Serializer):
    is_learning = serializers.BooleanField()
    register_date = serializers.DateTimeField()
    image = serializers.ImageField()
    animal_id = serializers.CharField()

    class Meta:
        model = AnimalImage
        fields = '__all__'
