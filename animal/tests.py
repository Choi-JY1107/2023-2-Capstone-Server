import io

from django.test import TestCase, Client
from rest_framework import status

from animal.models import Animal, AnimalImage
from users.models import User
from PIL import Image


class AnimalCreateViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='testUser', password='testUser')
        login_path = "/user/login"
        login_data = {"username": "testUser", "password": "testUser"}
        login_response = self.client.post(login_path, login_data)
        token = login_response.json()['token']
        self.headers = {'Authorization': 'Bearer ' + token}

    def test_animal_view_can_create_instance(self):
        path = "/animal/create"
        data = {"nickname": "test"}
        response = self.client.post(path, data, headers=self.headers)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)


class AnimalInfoViewTestCase(TestCase):
    def setUp(self):
        self.animal_data = {"nickname": "test"}
        User.objects.create_user(username="testUser", password="testUser")
        Animal.create_animal(data=self.animal_data, user=User.objects.get(username="testUser"))

        login_path = "/user/login"
        login_data = {"username": "testUser", "password": "testUser"}
        login_response = self.client.post(login_path, login_data)

        token = login_response.json()['token']
        self.headers = {'Authorization': 'Bearer ' + token}

    def test_animal_info_view_can_find_instance(self):
        info_path = "/animal/1"
        info_response = self.client.get(path=info_path, headers=self.headers)
        self.assertEquals("test", info_response.json()['data']['nickname'])

    def test_animal_info_view_can_check_pk(self):
        info_path = "/animal/10"
        info_response = self.client.get(path=info_path, headers=self.headers)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, info_response.status_code)


class AnimalImageCreateViewTestCase(TestCase):
    def setUp(self):
        animal_data = {"nickname": "test"}
        User.objects.create_user(username="testUser", password="testUser")
        Animal.create_animal(data=animal_data, user=User.objects.get(username="testUser"))

        login_path = "/user/login"
        login_data = {"username": "testUser", "password": "testUser"}
        login_response = self.client.post(login_path, login_data)
        token = login_response.json()['token']
        self.headers = {'Authorization': 'Bearer ' + token}

        self.file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(self.file, 'png')
        self.file.seek(0)

    def test_animal_image_view_can_create_instance(self):
        image_path = "/animal/image/create"
        image_data = {"animal_id": "1", "image": self.file}
        image_response = self.client.post(image_path, image_data, headers=self.headers)
        self.assertEquals(status.HTTP_201_CREATED, image_response.status_code)


class AnimalImageInfoViewTestCase(TestCase):
    def setUp(self):
        # 로그인 토큰
        animal_data = {"nickname": "test"}
        User.objects.create_user(username="testUser", password="testUser")
        Animal.create_animal(data=animal_data, user=User.objects.get(username="testUser"))
        login_path = "/user/login"
        login_data = {"username": "testUser", "password": "testUser"}
        login_response = self.client.post(login_path, login_data)
        token = login_response.json()['token']
        self.headers = {'Authorization': 'Bearer ' + token}

        # 사진 저장
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.seek(0)

        image_path = "/animal/image/create"
        image_data = {"animal_id": "1", "image": file}
        self.client.post(image_path, image_data, headers=self.headers)

    def test_animal_image_view_can_find_instance(self):
        image_path = "/animal/image/1"
        image_response = self.client.get(image_path, headers=self.headers)
        self.assertEquals(status.HTTP_200_OK, image_response.status_code)

