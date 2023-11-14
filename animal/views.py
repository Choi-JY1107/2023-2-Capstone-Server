from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from animal.models import Animal, AnimalImage
from animal.serializers import AnimalInfoSerializer, AnimalImageSerializer
from users.models import User


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
            serializer = AnimalInfoSerializer(animal)
            return JsonResponse(data={"data": serializer.data, "message": "Animal Info Success"}, status=200)

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DetailAnimalImageAPI(APIView):

    @staticmethod
    def get(request, pk):
        try:
            animal_image = AnimalImage.objects.get(id=pk)
            serializer = AnimalImageSerializer(animal_image)
            return JsonResponse(data={"data": serializer.data, "message": "Animal Image Success"}, status=200)
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


class ListAnimalAPI(APIView):

    @staticmethod
    def get(request):
        try:
            animal = Animal.objects.all()
            serializer = AnimalInfoSerializer(animal, many=True)
            return JsonResponse(data={"data": serializer.data, "message": "Animal List Success"}, status=200)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListAnimalImageAPI(APIView):

    @staticmethod
    def get(request, pk):
        try:
            animal = Animal.objects.get(id=pk)
            animal_images = AnimalImage.objects.filter(animal_id=animal)
            serializer = AnimalImageSerializer(animal_images, many=True)

            return JsonResponse(data={"data": serializer.data, "message": "Animal Image List Success"}, status=200)

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListMyAnimalAPI(APIView):

    @staticmethod
    def get(request):
        try:
            print(type(request.user))
            animal = Animal.objects.filter(owner=request.user)
            serializer = AnimalInfoSerializer(animal, many=True)
            return JsonResponse(data={"data": serializer.data, "message": "Animal List Success"}, status=200)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListAllAnimalAPI(APIView):
    @staticmethod
    def get(request):
        try:
            manager = User.objects.get(id=1)
            if request.user != manager:
                raise Exception("관리자만 사용 가능한 api입니다.")
            animal_image = AnimalImage.objects.all()
            serializer = AnimalImageSerializer(animal_image, many=True)
            return JsonResponse(data={"data": serializer.data, "message": f"{len(serializer.data)}개의 데이터를 불러왔습니다."},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
