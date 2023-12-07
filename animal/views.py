from rest_framework.views import APIView

from animal.models import Animal, AnimalImage
from animal.serializers import AnimalInfoSerializer, AnimalImageSerializer
from posts.models import PostAlarm
from users.models import User, UserDevice
from users.serializers import UserInfoSerializer
from util.response_format import response
from util.send_to_firebase_cloud_messaging import send_to_firebase_cloud_messaging


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
            user = animal.owner
            animal_serializer = AnimalInfoSerializer(animal)

            if not user.personal_consent:
                user.phone_number = None
            user_serializer = UserInfoSerializer(user)

            data = {'animal': animal_serializer.data,
                    'user': user_serializer.data}

            return response(
                data=data,
                message="id = %d인 유저가 id = %d인 Animal 정보를 불러왔습니다." % (request.user.id, pk),
                status=200
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )

    @staticmethod
    def put(request, pk):
        try:
            animal = Animal.objects.get(id=pk)

            if animal.owner != request.user:
                raise Exception("자신의 반려 동물의 정보만 수정할 수 있습니다.")

            nickname = request.data['nickname']
            characteristic = request.data['characteristic']
            animal.nickname = nickname
            animal.characteristic = characteristic
            animal.save()

            serializer = AnimalInfoSerializer(animal)

            return response(
                data=serializer.data,
                message="id = %d인 동물의 정보를 수정하였습니다." % pk,
                status=200
            )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )

    @staticmethod
    def delete(request, pk):
        try:
            animal = Animal.objects.get(id=pk)

            if animal.owner != request.user:
                raise Exception("자신의 반려 동물 정보만 삭제할 수 있습니다.")

            serializer = AnimalInfoSerializer(animal)
            animal.delete()

            return response(
                data=serializer.data,
                message="id = %d인 동물의 정보를 삭제하였습니다." % pk,
                status=200
            )

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


class ChangeAnimalImageAPI(APIView):

    @staticmethod
    def get(request, pk):
        try:
            animal_image = AnimalImage.objects.get(id=pk)
            animal = Animal.objects.get(id=animal_image.animal_id.id)
            if animal.owner != request.user:
                raise Exception("자신의 반려 동물 대표 이미지만 수정할 수 있습니다.")

            animal.main_img_id = pk
            animal.main_img = str(animal_image)
            animal.save()

            return response(
                message="id = %d인 유저가 id = %s인 Animal Image를 대표 이미지로 변경하였습니다."
                        % (request.user.id, animal_image.id),
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
                message="id = %s인 동물의 사진 리스트를 불러왔습니다." % pk,
                status=200
            )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class AlertMissingAPI(APIView):
    @staticmethod
    def post(request):
        try:
            animal_id = request.data['animal_id']
            animal_location = request.data['missing_location']
            animal = Animal.objects.get(id=animal_id)
            if animal.owner != request.user:
                raise Exception("자신의 반려동물만 실종 신고할 수 있습니다.")
            animal.is_missing = True
            animal.missing_location = animal_location
            animal.save()

            # TODO 사용자 위치 정보에 알맞는 사람만 알림 보내는 로직 추가
            title = "실종 신고"
            body = f"'{animal.nickname}' 이름을 가진 동물을 찾습니다."
            link = "http:127.0.0.1:8000/login"

            device_list = UserDevice.objects.all()
            for device in device_list:
                send_to_firebase_cloud_messaging(device.fcm_token, title, body, link)

            user_list = User.objects.all()
            for user in user_list:
                if user == request.user:
                    continue

                post_alarm = PostAlarm.objects.filter(
                    target_username=user.username,
                    register_username=request.user.username,
                    content_type=1,
                    content_id=int(animal_id)
                )
                if post_alarm.exists():
                    continue

                PostAlarm.create_user_alarm(
                    user.username,
                    request.user.username,
                    1,
                    int(animal_id)
                )

            return response(
                message=f"{len(user_list) - 1}개의 디바이스에 id = %s인 동물의 실종 알림을 전송하였습니다." % animal_id,
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


class ListMyAnimalImageAPI(APIView):
    @staticmethod
    def get(request):
        try:
            user = request.user
            animals = Animal.objects.filter(owner=user)
            my_animals = list(map(lambda x: x.id, animals))

            result = []
            for my_animal_id in my_animals:
                animal_image = AnimalImage.objects.filter(animal_id=my_animal_id)
                serializer = AnimalImageSerializer(animal_image, many=True)
                result.append(serializer.data)

            return response(
                data=result,
                message=f"{len(result)}마리 동물의 데이터를 불러왔습니다.",
                status=200
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )

class FoundMyPetAPI(APIView):
    @staticmethod
    def get(request, pk):
        try:
            animal = Animal.objects.get(id=pk)
            if animal.owner != request.user:
                raise Exception("자신의 반려동물만 실종 신고 해제할 수 있습니다.")

            post_alarms = PostAlarm.objects.filter(
                register_username=request.user.username,
                content_type=1,
                content_id=int(pk)
            )
            for post_alarm in post_alarms:
                post_alarm.delete()

            return response(
                message="id = %s인 유저가 id = %s인 자신의 반려동물을 찾았습니다." % (request.user.id, pk),
                status=200
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )

