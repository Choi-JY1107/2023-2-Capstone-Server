from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings

from .models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16)
    nickname = serializers.CharField(max_length=20)
    phone_number = serializers.CharField(max_length=15)
    register_date = serializers.DateTimeField()
    profile_number = serializers.IntegerField()
    personal_consent = serializers.BooleanField()

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=8)
    password = serializers.CharField(max_length=32)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)

        if user is None:
            if User.objects.filter(username=username).exists():
                return {'message': 'Password is incorrect'}
            return {'message': 'There is no username.'}

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        update_last_login(None, user)
        return {'token': token}


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=5)
    nickname = serializers.CharField(max_length=8)
    password1 = serializers.CharField(max_length=32)
    password2 = serializers.CharField(max_length=32)
    phone_number = serializers.CharField(max_length=15)

    def validate(self, data):
        username = data.get("username", None)
        nickname = data.get("nickname", None)
        password1 = data.get("password1", None)
        password2 = data.get("password2", None)
        phone_number = data.get("phone_number", None)

        if User.objects.filter(username=username).exists():
            return {'message': 'Username Error'}
        if password1 != password2:
            return {'message': 'Password Error'}

        User.objects.create_user(
            username=username,
            nickname=nickname,
            password=password1,
            phone_number=phone_number
        )

        return {'message': 'SignUp Success'}
