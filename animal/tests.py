from django.test import TestCase, Client
from rest_framework import status

from animal.models import Animal
from users.models import User


class AnimalCreateViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='testUser', password='testUser')
        login_path = "/users/login/"
        login_data = {"username": "testUser", "password": "testUser"}
        login_response = self.client.post(login_path, login_data)
        token = login_response.json()['token']
        self.headers = {'Authorization': 'Bearer ' + token}

    def test_animal_view_can_create_instance(self):
        path = "/animal/create/"
        data = {"nickname": "test"}
        response = self.client.post(path, data, headers=self.headers)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)


class AnimalInfoViewTestCase(TestCase):
    def setUp(self):
        self.animal_data = {"nickname": "test"}
        User.objects.create_user(username="testUser", password="testUser")
        Animal.create_animal(data=self.animal_data, user=User.objects.get(username="testUser"))

        login_path = "/users/login/"
        login_data = {"username": "testUser", "password": "testUser"}
        login_response = self.client.post(login_path, login_data)

        token = login_response.json()['token']
        self.headers = {'Authorization': 'Bearer ' + token}

    def test_animal_info_view_can_find_instance(self):
        info_path = "/animal/info/1"
        info_response = self.client.get(path=info_path, headers=self.headers)
        self.assertEquals("test", info_response.json()['nickname'])

# class AnimalImageCreateViewTestCase(TestCase):
#     def setUpTestData(self):
#         self.login_path = "/users/login/"
#         self.login_data = {"username": "testUser", "password": "testUser"}
#         self.animal_path = "/animal/create/"
#         self.animal_data = {"nickname": "test"}
#         self.image_path = "/animal/image/"
#         self.image_data = {""}
