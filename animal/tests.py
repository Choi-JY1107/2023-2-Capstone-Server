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

        self.assertEquals(response.status_code, status.HTTP_200_OK)


class AnimalInfoViewTestCase(TestCase):
    def setUpTestData(self):
        self.login_path = "/users/login/"
        self.login_data = {"username": "testUser", "password": "testUser"}
        self.animal_path = "/animal/create/"
        self.animal_data = {"nickname": "test"}
        self.info_path = "/animal/info/1"

    def setUp(self):
        login_response = self.client.post(self.login_path, self.login_data)
        token = login_response.json()['token']
        self.headers = {'Authorization': 'Bearer ' + token}
        self.client.post(self.animal_path, self.animal_data, headers=self.headers)

    def test_animal_info_view_can_find_instance(self):
        info_response = self.client.get(path=self.info_path)
        self.assertEquals("test", info_response.json()['nickname'])