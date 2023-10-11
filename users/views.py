from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.serializers import UserInfoSerializer, LoginSerializer, SignupSerializer


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        try:
            serializer = LoginSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)

            if serializer.validated_data['message'] == 'success':
                return JsonResponse(data=serializer.validated_data, status=status.HTTP_200_OK)
            return JsonResponse(data=serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SignupAPI(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        try:
            serializer = SignupSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)

            if serializer.validated_data['message'] == 'SignUp Success':
                return JsonResponse(data=serializer.validated_data, status=status.HTTP_201_CREATED)
            return JsonResponse(data=serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoAPI(APIView):
    @staticmethod
    def get(request):
        try:
            serializer = UserInfoSerializer(request.user)

            return JsonResponse(data=serializer.data, safe=False)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
