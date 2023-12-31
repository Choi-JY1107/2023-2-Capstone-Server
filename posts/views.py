from rest_framework.views import APIView
from PIL import Image

from posts.models import Post, PostImage, MissingImage, PostAlarm
from posts.serializers import (FeedPostSerializer, FeedPostImageSerializer,
                               FeedWriteSerializer, MissingListSerializer,
                               PostAlarmListSerializer)
from animal.models import Animal
from animal.serializers import AnimalInfoSerializer
from users.models import User

from util.pet_classification import predict_pet
from util.response_format import response


class CreatePostAPI(APIView):

    @staticmethod
    def post(request):
        try:
            post = Post.create_post(data=request.data, user=request.user)
            images = request.data
            image_list = images.getlist('images')

            for image in image_list:
                PostImage.create_post_image(image, post)

            return response(
                data=post,
                message="id = %d인 User 가 id = %s인 post를 등록하였습니다." % (request.user.id, post),
                status=201
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class CreatePostImageAPI(APIView):
    @staticmethod
    def post(request):
        try:
            post_image = PostImage.create_post_image(request.data['animal_image_id'], request.data['post_id'])
            return response(
                message='id = %s인 Post에 id = %s인 Post 사진을 등록하였습니다.'
                        % (request.data['post_id'], post_image),
                status=201
            )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class CreateMissingAPI(APIView):
    @staticmethod
    def post(request):
        try:
            missing = MissingImage.create_missing_image(request.FILES['image'], request.user)

            image = Image.open(request.FILES['image'])
            expected_pet_list = predict_pet(image)
            result = []

            for index in expected_pet_list:
                animal = Animal.objects.filter(id=index[0])

                if len(animal) == 0:
                    continue
                if animal[0].is_missing:
                    serializer = AnimalInfoSerializer(animal[0])
                    result.append(serializer.data)

            if len(result) > 5:
                result = result[:5]

            return response(
                data=result,
                message=missing,
                status=201
            )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class ListMissingAPI(APIView):
    @staticmethod
    def get(request):
        try:
            missing = MissingImage.objects.all()
            serializer = MissingListSerializer(missing, many=True)
            return response(
                data=serializer.data,
                message='id = %d인 User가 실종 동물 사진 리스트를 등록하였습니다.'
                        % request.user.id,
                status=200
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class ListFeedsAPI(APIView):
    @staticmethod
    def get(request):
        try:
            feed_list = []
            posts = Post.objects.all().order_by('-register_date')
            for post in posts:
                post_images = PostImage.objects.filter(post_id=post).order_by('register_date')
                register = post.register_id

                post_serializer = FeedPostSerializer(post)

                post_images_serializer = FeedPostImageSerializer(post_images, many=True)
                register_serializer = FeedWriteSerializer(register)
                feed = {"post": post_serializer.data, "images": post_images_serializer.data,
                        "user": register_serializer.data}
                feed_list.append(feed)
            return response(
                data=feed_list,
                message=f"{len(posts)}개의 피드를 불렀습니다",
                status=200
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class LikeAPI(APIView):
    @staticmethod
    def get(request, post_id):
        try:
            user = request.user
            post = Post.objects.get(id=post_id)

            if post.like_users.filter(id=user.id).exists():
                post.like_users.remove(user)
                print(post.register_id.username)
                print(request.user.username)
                post_alarm = PostAlarm.objects.get(
                    target_username=post.register_id.username,
                    register_username=request.user.username,
                    content_type=3,
                    content_id=int(post.id)
                )
                post_alarm.delete()
                message = "id = %s인 유저가 id = %s인 게시글의 좋아요를 취소하였습니다." % (user.id, post.id)
            else:
                post.like_users.add(user)
                PostAlarm.create_user_alarm(
                    post.register_id.username,
                    request.user.username,
                    3,
                    int(post.id)
                )
                message = "id = %s인 유저가 id = %s인 게시글의 좋아요를 눌렀습니다." % (user.id, post.id)

            return response(
                message=message,
                status=200
            )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class FindMissingAPI(APIView):
    @staticmethod
    def post(request):
        try:
            missing_id = request.data['missing_id']
            animal_id = request.data['animal_id']
            find_location = request.data['find_location']
            find_phone_number = request.data['find_phone_number']

            missing = MissingImage.objects.get(id=int(missing_id))
            missing.possibility_animal = Animal.objects.get(id=int(animal_id))
            missing.phone_number = find_phone_number
            missing.missing_location = find_location
            missing.save()

            PostAlarm.create_user_alarm(
                missing.possibility_animal.owner.username,
                request.user.username,
                2,
                int(missing.id)
            )

            return response(
                message='id = %s인 실종 신고 정보를 주인에게 알렸습니다.' % missing_id,
                status=200
            )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class ListAlarmAPI(APIView):
    @staticmethod
    def get(request):
        try:
            alarm_list = PostAlarm.objects.filter(target_username=request.user.username).order_by('-register_date')
            serializer = PostAlarmListSerializer(alarm_list, many=True)

            return response(
                data=serializer.data,
                message=f"{len(alarm_list)}개의 피드를 불렀습니다",
                status=200
            )
        except Exception as e:
            return response(
                message=str(e),
                status=400
            )


class DetailAlarmAPI(APIView):
    @staticmethod
    def get(request, pk):
        try:
            alarm = PostAlarm.objects.get(id=pk)
            print(alarm.content_type)

            if alarm.content_type == 1:
                animal = Animal.objects.get(id=alarm.content_id)
                result = {
                    "main_img": animal.main_img,
                    "nickname": animal.nickname,
                    "location": animal.missing_location,
                    "phone_number": animal.owner.phone_number,
                    "characteristic" : animal.characteristic
                }

                return response(
                    data=result,
                    message="id = %d인 알람 내용을 요청하였습니다." % pk,
                    status=200
                )

            if alarm.content_type == 2:
                missing = MissingImage.objects.get(id=alarm.content_id)
                animal = missing.possibility_animal
                result = {
                    "main_img": missing.image.name,
                    "nickname": animal.nickname,
                    "location": missing.missing_location,
                    "phone_number": missing.phone_number,
                }

                return response(
                    data=result,
                    message="id = %d인 알람 내용을 요청하였습니다." % pk,
                    status=200
                )
            if alarm.content_type == 3:
                return response(
                    message=alarm.alarm_message,
                    status=200
                )

        except Exception as e:
            return response(
                message=str(e),
                status=400
            )
