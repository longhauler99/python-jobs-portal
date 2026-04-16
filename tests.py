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