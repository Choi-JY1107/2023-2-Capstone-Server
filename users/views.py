from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer, LoginSerializer, SignupSerializer


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


class TestAPI(APIView):
    @staticmethod
    def get(request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)

        return JsonResponse({'data': serializer.data}, safe=False)
