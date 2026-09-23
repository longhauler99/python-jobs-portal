from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.password = "Test-password-123!"
        self.user = User.objects.create_user(
            email="existing@example.com",
            role="job_seeker",
            password=self.password,
        )

    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "email": self.user.email,
            "password": self.password,
        })

        self.assertRedirects(
            response, reverse("dashboard"),
            fetch_redirect_response=False,
        )
        self.assertEqual(
            self.client.session.get("_auth_user_id"),
            str(self.user.pk),
        )

    def test_login_invalid_password(self):
        response = self.client.post(reverse("login"), {
            "email": self.user.email,
            "password": "wrong-password",
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_signup_success(self):
        response = self.client.post(reverse("signup"), {
            "email": "new@example.com",
            "role": "job_seeker",
            "password": self.password,
            "password2": self.password,
        })

        self.assertRedirects(
            response, reverse("profile_detail"),
            fetch_redirect_response=False,
        )
        user = User.objects.get(email="new@example.com")
        self.assertEqual(user.role, "job_seeker")
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(
            self.client.session.get("_auth_user_id"), str(user.pk)
        )

    def test_signup_password_mismatch(self):
        response = self.client.post(reverse("signup"), {
            "email": "mismatch@example.com",
            "role": "job_seeker",
            "password": self.password,
            "password2": "different-password",
        })

        self.assertRedirects(
            response, reverse("signup"),
            fetch_redirect_response=False,
        )
        self.assertFalse(
            User.objects.filter(email="mismatch@example.com").exists()
        )

    def test_signup_rejects_invalid_role(self):
        response = self.client.post(reverse("signup"), {
            "email": "invalid@example.com",
            "role": "admin",
            "password": self.password,
            "password2": self.password,
        })

        self.assertRedirects(
            response, reverse("signup"),
            fetch_redirect_response=False,
        )
        self.assertFalse(
            User.objects.filter(email="invalid@example.com").exists()
        )

    def test_logout(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(
            response, reverse("login"),
            fetch_redirect_response=False,
        )
        self.assertNotIn("_auth_user_id", self.client.session)