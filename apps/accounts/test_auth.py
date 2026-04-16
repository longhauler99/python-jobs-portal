from django.test import TestCase
from django.contrib.auth.models import User

class LoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_user_can_login(self):
        response = self.client.login(
            username='testuser',
            password='testpassword'
        )
        self.assertTrue(response)


    def test_login_view(self):
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpassword'
        })

        self.assertEqual(response.status_code, 302)  # redirect after login

