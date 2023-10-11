from django.test import TestCase, Client
from rest_framework import status

from .models import User


class LoginViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='1test', password='1test')

    def test_view_can_do_success_login(self):
        path = "/users/login/"
        data = {"username": "1test", "password": "1test"}
        response = self.client.post(path, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_view_can_do_fail_login(self):
        path = "/users/login/"
        data = {"username": "1t", "password": "1test"}
        response = self.client.post(path, data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test1', password='test1')

    def test_user_model_can_create_an_instance(self):
        instance = User.objects.get(username='test1')
        self.assertIsInstance(instance, User)

    def test_user_model_can_check_wrong_instance(self):
        instance = User.objects.filter(username='none')
        self.assertEquals(instance.exists(), False)


class InfoViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='infoUser', password='infoUser')
        login_path = "/users/login/"
        login_data = {"username": "infoUser", "password": "infoUser"}

        login_response = self.client.post(login_path, login_data)
        token = login_response.json()['token']
        self.headers = {'Authorization': 'Bearer ' + token}

    def test_view_can_search_instance(self):
        info_path = "/users/info/"
        self.response = self.client.get(info_path, headers=self.headers)
        self.assertEquals('infoUser', self.response.json()['username'])
