from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterViewTests(APITestCase):
    """
    Tests for the RegisterView API endpoint.
    """

    def setUp(self):
        """
        Define the URL for the registration endpoint.
        """
        self.register_url = reverse("user-register")

    def test_register_user_successfully(self):
        """
        Test that a user can register successfully with valid data.
        """
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
            "role": "reader"
        }

        response = self.client.post(self.register_url, data, format="json", wsgi_url_scheme="https")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["username"], data["username"])
        self.assertEqual(response.data["role"], data["role"])

        # Ensure the user is actually created in the database
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_user_password_mismatch(self):
        """
        Test that registration fails if password and confirm_password do not match.
        """
        data = {
            "username": "failuser",
            "email": "failuser@example.com",
            "password": "StrongPass123",
            "confirm_password": "WrongPass123",
            "role": "author"
        }

        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_password", response.data)
        self.assertFalse(User.objects.filter(username="failuser").exists())

    def test_register_user_with_existing_email(self):
        """
        Test that registration fails if the email is already used.
        """
        # First, create a user
        User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="StrongPass123",
            role="reader"
        )

        data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
            "role": "author"
        }

        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_author_profile_created_on_register(self):
        """
        When an author registers, AuthorProfile should be created automatically.
        """
        data = {
            "username": "author_user",
            "email": "author@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
            "role": "author"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="author_user")
        self.assertTrue(hasattr(user, "authorprofile"))
        self.assertFalse(hasattr(user, "readerprofile"))

    def test_reader_profile_created_on_register(self):
        """
        When a reader registers, ReaderProfile should be created automatically.
        """
        data = {
            "username": "reader_user",
            "email": "reader@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
            "role": "reader"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="reader_user")
        self.assertTrue(hasattr(user, "readerprofile"))
        self.assertFalse(hasattr(user, "authorprofile"))