from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework import status

from users.forms import LoginForm, SignupForm
from users.models import User
from users.serializers import UserSerializer


class LoginAPI(APIView):
    def get(self, request):
        form = LoginForm()
        context = {"form": form}
        return render(request, "users/login.html", context)

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("/posts/feeds/")
            else:
                print("계정 정보가 틀렸습니다.")
                return HttpResponse("로그인에 실패하였습니다.")

        context = {"form": form}
        return render(request, "users/login.html", context)


class LogoutAPI(APIView):
    def get(self, request):
        print(request.session)
        # 로그아웃 했는 지
        if request.session:
            logout(request)
            return HttpResponse("로그아웃 성공!")
        return HttpResponse("로그아웃 실패!")


class SignupAPI(APIView):
    def get(self, request):
        form = SignupForm()
        context = {"form": form}
        return render(request, "users/signup.html", context)

    def post(self, request):
        form = SignupForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponse("회원가입 성공!")

        context = {"form": form}
        return HttpResponse("회원가입 실패!")


class TestAPI(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)

        return JsonResponse({'data' : serializer.data}, safe=False)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)
