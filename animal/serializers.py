from rest_framework import serializers

from .models import Animal, AnimalImage


class AnimalInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nickname = serializers.CharField(max_length=8)
    main_img_id = serializers.IntegerField()
    main_img = serializers.CharField(max_length=255)
    characteristic = serializers.CharField(max_length=500)

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
