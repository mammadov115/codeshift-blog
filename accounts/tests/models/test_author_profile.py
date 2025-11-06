from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import AuthorProfile

User = get_user_model()


class AuthorProfileTest(TestCase):
    """Tests for the AuthorProfile model."""

    def setUp(self):
        self.user = User.objects.create_user(username="author1", password="pass123")
        self.author_profile = AuthorProfile.objects.create(
            user=self.user,
            bio="Tech enthusiast and backend developer.",
            website="https://example.com",
            verified=True,
            total_posts=5
        )

    def test_author_profile_creation(self):
        """Ensure an author profile is created and linked to the user."""
        self.assertEqual(self.author_profile.user.username, "author1")
        self.assertTrue(self.user.is_author)
        self.assertEqual(self.author_profile.bio, "Tech enthusiast and backend developer.")
        self.assertEqual(self.author_profile.total_posts, 5)
        self.assertTrue(self.author_profile.verified)

    def test_str_method_returns_author_name(self):
        """Check string representation of author profile."""
        self.assertEqual(str(self.author_profile), "Author: author1")

