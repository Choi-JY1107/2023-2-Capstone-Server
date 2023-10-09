from rest_framework import serializers
from django.contrib.auth import authenticate
from datetime import datetime

from .models import User


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=5)
    password = serializers.CharField(max_length=32)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)

        if user is None:
            return {'message': 'fail', 'username': username}
        user.last_login = datetime.now()
        user.save()
        return {'message': 'success', 'username': username}
#
#
# class SignupSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=5)
#     nickname = serializers.CharField(max_length=8)
#     password = serializers.CharField(max_length=32)
#     phone_number = serializers.CharField(max_length=15)
#
#     def validate_username(self, username) :
#         if User.objects.filter(username=username).exists():
#             raise serializers.ValidationError(
#                 detail="이미 존재하는 username 입니다."
#             )
#         return username
#
#     def validate_password(self, password):
#
#     def create(self, validated_data):
#         username = validated_data.get("username", None)
#         nickname = validated_data.get("nickname", None)
#         password = validated_data.get("password1", None)
#         phone_number = validated_data.get("phone_number", None)
#
#         User.objects.create_user(
#             username=username,
#             nickname=nickname,
#             password=password,
#             phone_number=phone_number
#         )
#         return {'message': '성공!'}
#
#     def validate(self, data):
#         print("엥?")
#         username = data.get("username", None)
#         password1 = data.get("password1", None)
#         password2 = data.get("password2", None)
#
#         if password1 != password2:
#             return {'message': '두 비밀번호가 다릅니다.'}
#
#         return {'message': '오류가 없습니다.'}
#
#     class Meta:
#         model = User
#         fields = '__all__'