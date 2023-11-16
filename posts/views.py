from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from PIL import Image

from posts.models import Post, PostImage, MissingImage
from posts.serializers import FeedPostSerializer, FeedPostImageSerializer, MissingListSerializer
from animal.models import Animal
from animal.serializers import AnimalInfoSerializer
from users.models import UserDevice

from util.send_to_firebase_cloud_messaging import send_to_firebase_cloud_messaging
from util.pet_classification import predict_pet


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


class CreatePostImageAPI(APIView):
    @staticmethod
    def post(request):
        try:
            post_image = PostImage.create_post_image(request.FILES['image'], request.data['post_id'])
            return JsonResponse(data={'message': 'id = %s인 Post에 id = %s인 Post 사진을 등록하였습니다.'
                                                 % (request.data['post_id'], post_image)},
                                status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateMissingAPI(APIView):
    @staticmethod
    def post(request):
        try:
            missing = MissingImage.create_missing_image(request.FILES['image'], request.user)

            image = Image.open(request.FILES['image'])
            expected_pet_list = predict_pet(image)

            result = []
            for index in expected_pet_list:
                animal = Animal.objects.get(id=index[0])
                if animal.is_missing:
                    serializer = AnimalInfoSerializer(animal)
                    result.append(serializer.data)

            if len(result) > 5:
                result = result[:5]
            return JsonResponse(data={'message': 'id = %d인 User가 id = %d인 실종 사진을 등록하였습니다.'
                                                 % (request.user.id, missing),
                                      "rank": result},
                                status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListMissingAPI(APIView):
    @staticmethod
    def get(request):
        try:
            missing = MissingImage.objects.all()
            serializer = MissingListSerializer(missing, many=True)
            return JsonResponse(data={"data": serializer.data, "message": "Missing List Success"},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AlertMissingAPI(APIView):
    @staticmethod
    def post(request):
        try:
            animal_id = request.data['animal_id']
            animal_location = request.data['missing_location']
            animal = Animal.objects.get(id=animal_id)
            if animal.owner != request.user:
                raise Exception("It is not your animal")
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

            return JsonResponse(data={"message": f"{len(device_list)}개의 디바이스에 알림 전송 완료"}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListFeedsAPI(APIView):
    @staticmethod
    def get(request):
        try:
            feed_list = []
            posts = Post.objects.all().order_by('register_date')
            for post in posts:
                post_images = PostImage.objects.filter(post_id=post).order_by('register_date')
                post_serializer = FeedPostSerializer(post)
                post_images_serializer = FeedPostImageSerializer(post_images, many=True)
                feed = {"post": post_serializer.data, "images": post_images_serializer.data}
                feed_list.append(feed)
            return JsonResponse(data={"feeds": feed_list, "message": f"{len(posts)}개의 피드를 불렀습니다"},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
