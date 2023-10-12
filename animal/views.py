from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from animal.models import Animal, AnimalImage
from animal.serializers import AnimalInfoSerializer


# animal 관련
class CreateAnimalAPI(APIView):

    @staticmethod
    def post(request):
        try:
            animal = Animal.create_animal(data=request.data, user=request.user)
            return JsonResponse(
                data={'message': "id = %d인 User 가 id = %s인 Animal을 등록하였습니다." % (request.user.id, animal)},
                status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateAnimalImageAPI(APIView):
    @staticmethod
    def post(request):
        try:
            AnimalImage.create_animal_image(request.FILES['image'], request.data['animal_id'])
            return JsonResponse(data={'message': 'id = %d인 User가 id = %s인 Animal의 사진 한 장을 등록하였습니다.'
                                                 % (request.user.id, request.data['animal_id'])},
                                status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DetailAnimalAPI(APIView):
    @staticmethod
    def get(request, pk):
        try:
            animal = Animal.objects.get(id=pk)

            if animal is None:
                return JsonResponse(data={"message": "There is no animal whose id is %d" + pk},
                                    status=status.HTTP_400_BAD_REQUEST)

            serializer = AnimalInfoSerializer(animal)
            return JsonResponse(data={"data": serializer.data, "message": "Animal Info Success"}, status=200)

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# TODO
class DetailAnimalImageAPI(APIView):

    @staticmethod
    def get(request, pk):
        try:
            animal_image = AnimalImage.objects.get(id=pk)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# TODO
class DeleteAnimalAPI(APIView):

    @staticmethod
    def delete(request):
        try:
            pass

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# TODO
class DeleteAnimalImageAPI(APIView):

    @staticmethod
    def delete(request):
        try:
            pass

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
