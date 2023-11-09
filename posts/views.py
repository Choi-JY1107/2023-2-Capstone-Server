from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from posts.models import Post, MissingImage


# Post 관련
class CreatePostAPI(APIView):

    @staticmethod
    def post(request):
        try:
            post = Post.create_post(data=request.data, user=request.user)
            return JsonResponse(
                data={'message': "id = %d인 User 가 id = %s인 post를 등록하였습니다." % (request.user.id, post)},
                status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateMissingAPI(APIView):
    @staticmethod
    def post(request):
        try:
            print(1231223)
            missing = MissingImage.create_missing_image(request.FILES['image'], request.user)
            print(323232)
            return JsonResponse(data={'message': 'id = %d인 User가 id = %d인 실종 사진을 등록하였습니다.'
                                                 % (request.user.id, missing)},
                                status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
