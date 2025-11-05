from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import AuthorProfile, ReaderProfile

User = get_user_model()


class UserModelTest(TestCase):
    """Tests for the custom User model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="strongpassword123"
        )

    def test_user_creation(self):
        """Check if a user is created correctly."""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("strongpassword123"))
        self.assertFalse(self.user.is_author)
        self.assertFalse(self.user.is_reader)

    def test_str_method_returns_username(self):
        """Ensure the string representation returns the username."""
        self.assertEqual(str(self.user), "testuser")