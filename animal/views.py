from rest_framework.views import APIView

from animal.models import Animal, AnimalImage
from animal.serializers import AnimalInfoSerializer, AnimalImageSerializer
from users.models import User
from util.response_format import response


# animal 관련
class CreateAnimalAPI(APIView):

    @staticmethod
    def post(request):
        try:
            animal = Animal.create_animal(data=request.data, user=request.user)
            return response(
                message="id = %d인 User 가 id = %s인 Animal을 등록하였습니다." % (request.user.id, animal),
                status=201
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class DetailAnimalAPI(APIView):
    @staticmethod
    def get(request, pk):
        try:
            animal = Animal.objects.get(id=pk)
            serializer = AnimalInfoSerializer(animal)
            return response(
                data=serializer.data,
                message="id = %d인 유저가 id = %d인 Animal 정보를 불러왔습니다." % (request.user.id, pk),
                status=200
            )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )

    @staticmethod
    def delete(request):
        try:
            pass

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class CreateAnimalImageAPI(APIView):
    @staticmethod
    def post(request):
        try:
            animal_image = AnimalImage.create_animal_image(request.FILES['image'], request.data['animal_id'])
            return response(
                message='id = %d인 User가 id = %s인 Animal의 id = %s인 사진 한 장을 등록하였습니다.'
                        % (request.user.id, request.data['animal_id'], animal_image),
                status=201
            )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class DetailAnimalImageAPI(APIView):

    @staticmethod
    def get(request, pk):
        try:
            animal_image = AnimalImage.objects.get(id=pk)
            serializer = AnimalImageSerializer(animal_image)
            return response(
                data=serializer.data,
                message="id = %d인 유저가 id = %s인 Animal Image를 요청하였습니다."
                        % (request.user.id, animal_image),
                status=200)
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )

    @staticmethod
    def delete(request):
        try:
            pass

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class ListAnimalAPI(APIView):

    @staticmethod
    def get(request):
        try:
            animal = Animal.objects.filter(owner=request.user)
            serializer = AnimalInfoSerializer(animal, many=True)
            return response(
                data=serializer.data,
                message="id = %d인 유저가 자신의 반려동물 리스트를 요청하였습니다."
                        % request.user.id,
                status=200
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class ListAnimalImageAPI(APIView):

    @staticmethod
    def get(request, pk):
        try:
            animal = Animal.objects.get(id=pk)
            animal_images = AnimalImage.objects.filter(animal_id=animal)
            serializer = AnimalImageSerializer(animal_images, many=True)

            return response(
                data=serializer.data,
                message="Animal Image List Success",
                status=200
            )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class ListAllAnimalAPI(APIView):
    @staticmethod
    def get(request):
        try:
            manager = User.objects.get(id=1)
            if request.user != manager:
                raise Exception("관리자만 사용 가능한 api입니다.")
            animal_image = AnimalImage.objects.all()
            serializer = AnimalImageSerializer(animal_image, many=True)
            return response(
                data=serializer.data,
                message=f"{len(serializer.data)}개의 데이터를 불러왔습니다.",
                status=200
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )
