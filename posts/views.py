from rest_framework.views import APIView
from PIL import Image

from posts.models import Post, PostImage, MissingImage
from posts.serializers import (FeedPostSerializer, FeedPostImageSerializer,
                               FeedWriteSerializer, FeedSerializer,
                               MissingListSerializer)
from animal.models import Animal
from animal.serializers import AnimalInfoSerializer
from users.models import UserDevice, User

from util.send_to_firebase_cloud_messaging import send_to_firebase_cloud_messaging
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
                animal = Animal.objects.get(id=index[0])
                if animal.is_missing:
                    serializer = AnimalInfoSerializer(animal)
                    result.append(serializer.data)

            if len(result) > 5:
                result = result[:5]
            return response(
                data=result,
                message='id = %d인 User가 id = %d인 실종 사진을 등록하였습니다.'
                        % (request.user.id, missing),
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
            posts = Post.objects.all().order_by('register_date')
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
                message = "id = %s인 유저가 id = %s인 게시글의 좋아요를 취소하였습니다." % (user.id, post.id)
            else:
                post.like_users.add(user)
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
