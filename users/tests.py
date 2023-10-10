from django.test import TestCase, Client
from rest_framework import status
from .models import User


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.instance = User.objects.create_user(username='1test', password='1test')

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

