from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from users.serializers import UserInfoSerializer, LoginSerializer, SignupSerializer
from util.response_format import response


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        try:
            serializer = LoginSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)

            if 'token' in serializer.validated_data:
                return response(
                    data=serializer.validated_data,
                    message='Login Success',
                    status=200
                )
            return response(
                message=serializer.validated_data['message'],
                status=400
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class SignupAPI(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        try:
            serializer = SignupSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)

            if serializer.validated_data['message'] == 'SignUp Success':
                return response(
                    message=serializer.validated_data['message'],
                    status=201
                )
            return response(
                message=serializer.validated_data['message'],
                status=400
            )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class UserInfoAPI(APIView):
    @staticmethod
    def get(request):
        try:
            serializer = UserInfoSerializer(request.user)

            return response(
                data=serializer.data,
                message='id = %d인 유저가 정보를 요청하였습니다.' % request.user.id,
                status=200
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )

    @staticmethod
    def patch(request):
        try:
            user = request.user
            data = request.data
            print(user.username)
            serializer = UserInfoSerializer(user, data=data)

            if serializer.is_valid():
                print(123)
                serializer.save()

            print(serializer.data)

            return response(
                data=serializer.validated_data,
                message='id = %d인 유저가 정보를 변경하였습니다.' % request.user.id,
                status=200
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


