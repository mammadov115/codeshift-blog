from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginViewTests(APITestCase):
    """
    Test suite for the LoginView API endpoint.
    """

    def setUp(self):
        """
        Create a test user and define login URL.
        """
        self.login_url = reverse("user-login")
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="StrongPass123",
            role="author"
        )

    def test_login_successful(self):
        """
        Test that a user can login successfully and receive JWT tokens.
        """
        data = {
            "username": "testuser",
            "password": "StrongPass123"
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["role"], self.user.role)

    def test_login_invalid_credentials(self):
        """
        Test login fails with incorrect username or password.
        """
        data = {
            "username": "testuser",
            "password": "WrongPass123"
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data or "detail")  # serializer validation error

    def test_login_requires_username_and_password(self):
        """
        Test login fails if username or password is missing.
        """
        data = {"username": "testuser"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"password": "StrongPass123"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_cannot_access_login(self):
        """
        Test that already authenticated users cannot access the login endpoint.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "username": "testuser",
            "password": "StrongPass123"
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
