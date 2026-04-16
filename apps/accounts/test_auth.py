# from django.test import TestCase
# from django.contrib.auth.models import User
# from django.urls import reverse


# class AuthTests(TestCase):

#     def setUp(self):
#         self.email = "olesaina@gmail.com"
#         self.password = "testpassword123"

#         self.user = User.objects.create_user(
#             username=self.email,   # email used as username
#             email=self.email,
#             password=self.password
#         )

#     # ======================
#     # LOGIN TESTS
#     # ======================

#     def test_user_can_login_with_client(self):
#         login = self.client.login(
#             username=self.email,
#             password=self.password
#         )
#         self.assertTrue(login)

#     def test_login_view_success(self):
#         response = self.client.post(reverse('login'), {
#             'email': self.email,
#             'password': self.password
#         })

#         self.assertRedirects(response, reverse('jobs'))

#     def test_login_view_invalid_credentials(self):
#         response = self.client.post(reverse('login'), {
#             'email': self.email,
#             'password': 'wrongpassword'
#         })

#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Invalid")

#     def test_logged_in_user_cannot_access_login(self):
#         self.client.login(username=self.email, password=self.password)

#         response = self.client.get(reverse('login'))

#         self.assertRedirects(response, reverse('jobs'))

#     # ======================
#     # SIGNUP TESTS
#     # ======================

#     def test_user_can_signup(self):
#         response = self.client.post(reverse('signup'), {
#             'first_name': 'Ole',
#             'last_name': 'Saina',
#             'email': 'newuser@gmail.com',
#             'password': 'newpassword123',
#             'password2': 'newpassword123'
#         })

#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(User.objects.filter(email='newuser@gmail.com').exists())

#     def test_signup_password_mismatch(self):
#         response = self.client.post(reverse('signup'), {
#             'first_name': 'Ole',
#             'last_name': 'Saina',
#             'email': 'failuser@gmail.com',
#             'password': 'pass123',
#             'password2': 'wrongpass'
#         })

#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(User.objects.filter(email='failuser@gmail.com').exists())

#     def test_logged_in_user_cannot_access_signup(self):
#         self.client.login(username=self.email, password=self.password)

#         response = self.client.get(reverse('signup'))

#         self.assertRedirects(response, reverse('jobs'))

#     # ======================
#     # LOGOUT TEST
#     # ======================

#     def test_user_can_logout(self):
#         self.client.login(username=self.email, password=self.password)

#         response = self.client.post(reverse('logout'))

#         self.assertRedirects(response, reverse('login'))