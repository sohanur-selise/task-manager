from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from rest_framework.authtoken.models import Token
import json
from tasks.models import Task


class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_url = reverse('tasks_api:task_create')
        self.task_retrieve_url = reverse('tasks_api:task_retrieve', args=[1])  # Assuming task ID 1 exists
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        self.task = Task.objects.create(
            name='test task',
            description='demo',
            due_date='2023-06-30'
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)

        # URL name from urls.py
        self.assignee_id = 1
        self.task_data = {
            'name': 'Test Task',
            'description': 'test description',
            'assignee': self.user.id,
            'due_date': '2023-06-30',
            'username': 'test_user'
        }

    def test_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.task_url, self.task_data)
        print(response.status_code)
        response_data = json.loads(response.content)
        response_data = response_data['data']
        print(response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(self.task_retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        response_data = response_data['data']
        print(response_data)
    #
    # # Add more test methods for other actions like update, delete, etc.


class CommentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_id = 1  # ID of an existing task
        self.comments_url = reverse('tasks_api:task-comments-list', args=[self.task_id])  # URL name from urls.py
        self.comment_data = {
            'content': 'Test Comment',
            # Include other required fields for Comment creation
        }
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.task = Task.objects.create(
            name='test task',
            description='demo',
            due_date='2023-06-30'
        )

        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_create_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.comments_url, self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Additional assertions to verify the response or database changes

    def test_list_comments(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(self.comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

