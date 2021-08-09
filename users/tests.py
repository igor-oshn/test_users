from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate


class UserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Test', is_active=True)
        cls.user.set_password('Azds213123')
        cls.user.save()
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_token_auth_valid(self):
        """
        Ensure we can authenticate Test user and get token.
        """
        url = reverse('api-token-auth')
        data = {'username': 'Test', 'password': 'Azds213123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], str(self.token))

    def test_create_user_valid(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('user-list')
        data = {'username': 'Test2', 'password': 'Azds213123', 'is_active': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, 'Test2')

    def test_create_user_invalid(self):
        """
        Ensure we can't create a new user without username.
        """
        url = reverse('user-list')
        data = {'username': '', 'password': 'Azds213123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_get_users(self):
        """
        Ensure we can get all users.
        """
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_user_detail_valid(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_put_valid(self):
        """
        Ensure we can update user.
        """
        url = reverse('user-detail',  kwargs={'id': self.user.id})
        data = {'username': 'Test', 'password': 'Azds213123', 'first_name': 'Test_first_name', 'is_active': True}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Test_first_name')

    def test_user_patch_valid(self):
        """
        Ensure we can partial update user.
        """
        url = reverse('user-detail',  kwargs={'id': self.user.id})
        data = {'username': 'Test', 'first_name': 'Test_first_name2'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Test_first_name2')

