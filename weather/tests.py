from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTest(APITestCase):
    """Класс для теста api автризации"""

    def setUp(self):
        self.url = reverse("registration")

    def test_valid_registration(self):
        data = {
            "username": "test@ya.ru",
            "password": "te!T_p@ssw0rd",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_registration(self):
        data = {
            "username": "test@ya.ru",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="test1", password="test1")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('weather'))

        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_login(self):
        self.client.login(username='test1', password='test1')
        response = self.client.get(reverse('weather'))

        self.assertEqual(str(response.context['user']), 'test1')
        self.assertEqual(response.status_code, 200)