from django.test import TestCase, Client
from rest_framework import status

from posts.models import Post
from users.models import User


class PostInstanceTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='testUser', password='testUser')
        login_path = "/user/login"
        login_data = {"username": "testUser", "password": "testUser"}
        login_response = self.client.post(login_path, login_data)
        token = login_response.json()['token']
        self.headers = {'Authorization': 'Bearer ' + token}

    def test_post_can_create_instance(self):
        user = User.objects.get(id=1)
        post = Post.objects.create(
            content='안녕하쇼',
            register_id=user
        )
        self.assertEquals(post.content, '안녕하쇼')


class PostCreateViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='testUser', password='testUser')
        login_path = "/user/login"
        login_data = {"username": "testUser", "password": "testUser"}
        login_response = self.client.post(login_path, login_data)
        token = login_response.json()['token']
        self.headers = {'Authorization': 'Bearer ' + token}

    def test_post_view_can_create_instance(self):
        path = "/post/create"
        data = {"content": "안녕하쇼"}
        response = self.client.post(path, data, headers=self.headers)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
