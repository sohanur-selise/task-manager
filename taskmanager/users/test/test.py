import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from users.models import User
from users.api.views import CustomObtainAuthToken, UserViewSet


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_list_users(self):
        view = UserViewSet.as_view({'get': 'list'})
        request = self.factory.get('/users/list')
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_user(self):
        view = UserViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/users/list/1')  # assuming user with pk=1 exists
        force_authenticate(request, user=self.user)  # authenticate the request
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        view = UserViewSet.as_view({'post': 'create'})
        request = self.factory.post('/users/register', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'role': 'user',
            'first_name': 'New',
            'last_name': 'User'
        })
        response = view(request)
        self.assertEqual(response.status_code, 200)


class CustomObtainAuthTokenTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_authenticate_user(self):
        view = CustomObtainAuthToken.as_view()
        request = self.factory.post('/users/login', {
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        response = view(request)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        response_data = response_data['data']
        print(response_data['token'])
        self.assertIn('token', response_data)

