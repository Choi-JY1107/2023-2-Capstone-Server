from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserInfoSerializer, LoginSerializer, SignupSerializer


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['message'] == 'fail':
            return JsonResponse(data=serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data['message'] == 'success':
            return JsonResponse(data=serializer.validated_data, status=status.HTTP_200_OK)


class SignupAPI(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        serializer = SignupSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['message'] == 'SignUp Success':
            return JsonResponse(data=serializer.validated_data, status=status.HTTP_201_CREATED)
        return JsonResponse(data=serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)


class UserInfoAPI(APIView):
    @staticmethod
    def get(request):
        try:
            user = User.objects.get(username=request.user)
            serializer = UserInfoSerializer(user)

            return JsonResponse(data=serializer.data, safe=False)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
