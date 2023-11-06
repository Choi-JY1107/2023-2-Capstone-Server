from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from posts.models import Post


# animal 관련
class CreateAnimalAPI(APIView):

    @staticmethod
    def post(request):
        try:
            animal = Post.create_animal(data=request.data, user=request.user)
            return JsonResponse(
                data={'message': "id = %d인 User 가 id = %s인 Animal을 등록하였습니다." % (request.user.id, animal)},
                status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
