from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from posts.models import Post, MissingImage
from posts.serializers import MissingListSerializer


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
            missing = MissingImage.create_missing_image(request.FILES['image'], request.user)
            return JsonResponse(data={'message': 'id = %d인 User가 id = %d인 실종 사진을 등록하였습니다.'
                                                 % (request.user.id, missing)},
                                status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListMissingAPI(APIView):
    @staticmethod
    def get(request):
        try:
            missing = MissingImage.objects.all()
            serializer = MissingListSerializer(missing, many=True)
            return JsonResponse(data={"data": serializer.data, "message": "Missing List Success"}, status=200)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
