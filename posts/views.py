from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from posts.models import Post, PostImage, MissingImage
from posts.serializers import FeedPostSerializer, FeedPostImageSerializer, MissingListSerializer
from animal.models import Animal
from users.models import UserDevice
from util.send_to_firebase_cloud_messaging import send_to_firebase_cloud_messaging


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
            post_serializer = FeedPostSerializer(posts)
            for post in posts:
                print(111111)
                post_images = PostImage.objects.filter(post_id=post).order_by('register_date')
                post_images_serializer = FeedPostImageSerializer(post_images, many=True)
                feed = {"post": post_serializer, "images": post_images_serializer}
                feed_list.insert(feed)

                return JsonResponse(data={"message": f"{len(posts)}개의 피드를 불렀습니다"}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
