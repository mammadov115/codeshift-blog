from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import ReaderProfile

User = get_user_model()

class ReaderProfileTest(TestCase):
    """Tests for the ReaderProfile model."""

    def setUp(self):
        self.user = User.objects.create_user(username="reader1", password="pass123")
        self.reader_profile = ReaderProfile.objects.create(
            user=self.user,
            subscribed=True
        )

    def test_reader_profile_creation(self):
        """Ensure a reader profile is created and linked to the user."""
        self.assertEqual(self.reader_profile.user.username, "reader1")
        self.assertTrue(self.user.is_reader)
        self.assertTrue(self.reader_profile.subscribed)

    def test_str_method_returns_reader_name(self):
        """Check string representation of reader profile."""
        self.assertEqual(str(self.reader_profile), "Reader: reader1")

    # def test_reader_can_have_favorite_posts(self):
    #     """Ensure favorite_posts relation works correctly."""
    #     # Import locally to avoid circular import
    #     from blog.models import Post  

    #     # Mock post creation
    #     post = Post.objects.create(
    #         title="Test Post",
    #         content="Sample content",
    #         author=self.user
    #     )

    #     self.reader_profile.favorite_posts.add(post)
    #     self.assertIn(post, self.reader_profile.favorite_posts.all())