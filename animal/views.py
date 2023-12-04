from rest_framework.views import APIView

from animal.models import Animal, AnimalImage
from animal.serializers import AnimalInfoSerializer, AnimalImageSerializer
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

            if not user.personal_consent :
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

            return response(
                message=f"{len(device_list)}개의 디바이스에 id = %s인 동물의 실종 알림을 전송하였습니다." % animal_id,
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
            # open_api_url = "http://aiopen.etri.re.kr:8000/ObjectDetect"
            # access_key = "8a7fab67-2d64-44f3-9cc0-5a555e252db0"
            # image_file_path = ""
            # image_type = "jpg"
            #
            # file = open(image_file_path, "rb")
            # imageContents = base64.b64encode(file.read()).decode("utf8")
            # file.close()
            #
            # requestJson = {
            #     "argument": {
            #         "type": image_type,
            #         "file": imageContents
            #     }
            # }
            #
            # http = urllib3.PoolManager()
            # http_response = http.request(
            #     "POST",
            #     open_api_url,
            #     headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": access_key},
            #     body=json.dumps(requestJson)
            # )
            #
            # print("[responseCode] " + str(http_response.status))
            # print("[responseBody]")
            # print(http_response.data)

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
