from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework import status

from users.forms import LoginForm, SignupForm
from users.models import User
from users.serializers import UserSerializer, LoginSerializer


class LoginAPI(APIView):
    def get(self, request):
        form = LoginForm()
        context = {"form": form}
        return render(request, "users/login.html", context)

    def post(self, request):
        serializer = LoginSerializer(data=request.POST)
        serializer.is_valid()

        if serializer.validated_data['message'] == 'fail':
            return JsonResponse(data=serializer.validated_data, status=400)
        if serializer.validated_data['message'] == 'success':
            print(serializer.validated_data['username'])
            user = User.objects.get(username=serializer.validated_data['username'])
            login(request, user)
            return JsonResponse(data=serializer.validated_data, status=200)
        # return render(request, "users/login.html", context)


class LogoutAPI(APIView):
    @staticmethod
    def get(self, request):
        print(request.session)
        # 로그아웃 했는 지
        if request.session:
            logout(request)
            return HttpResponse("로그아웃 성공!")
        return HttpResponse("로그아웃 실패!")


class SignupAPI(APIView):
    @staticmethod
    def get(self, request):
        form = SignupForm()
        context = {"form": form}
        return render(request, "users/signup.html", context)

    @staticmethod
    def post(self, request):
        print(dict(request.data))
        username = request.data['username']
        nickname = request.data['nickname']
        password1 = request.data['password1']
        password2 = request.data['password2']
        phone_number = request.data['phone_number']

        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': '이미 존재하는 계정입니다.'}, status=400)
        if password1 != password2:
            return JsonResponse({'message': '비밀번호가 일치하지 않습니다.'}, status=400)

        User.objects.create_user(
            username=username,
            nickname=nickname,
            password=password1,
            phone_number=phone_number
        )
        return JsonResponse({'message': '회원가입에 성공하였습니다'}, status=201)


class TestAPI(APIView):
    @staticmethod
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)

        return JsonResponse({'data': serializer.data}, safe=False)

    @staticmethod
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)
