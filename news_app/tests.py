from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .models import News


class NewsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='tester@example.com', password='password123')
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_news_authenticated(self):
        url = reverse('news-list')
        payload = {
            'title': 'API test news',
            'summary': 'Short summary',
            'content': 'A' * 60,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(News.objects.first().author, self.user)

    def test_list_news_by_author_filter(self):
        News.objects.create(title='By user', summary='Summary', content='B' * 60, author=self.user)
        other = User.objects.create_user(username='other', email='other@example.com', password='password123')
        News.objects.create(title='By other', summary='Summary', content='C' * 60, author=other)
        url = reverse('news-list') + f'?author={self.user.id}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class UserAPITestCase(APITestCase):
    def test_register_user(self):
        url = reverse('user-list')
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
