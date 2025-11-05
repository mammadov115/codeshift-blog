from django.test import TestCase
from django.contrib.auth import get_user_model
from blogs.models import Post, Comment, Category

User = get_user_model()


class CommentModelTest(TestCase):
    """Test suite for the Comment model."""

    def setUp(self):
        """Create initial test data."""
        self.user = User.objects.create_user(username="testuser", password="securepassword123")
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            author=self.user,
            status="published",
            category=self.category
        )

    def test_create_comment(self):
        """Should successfully create a top-level comment."""
        comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content="This is a comment."
        )
        self.assertEqual(comment.content, "This is a comment.")
        self.assertTrue(comment.is_parent())
        self.assertEqual(str(comment), f"Comment by {self.user} on {self.post}")

    def test_nested_comment(self):
        """Should correctly handle nested (reply) comments."""
        parent_comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content="Parent comment"
        )
        reply_comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content="Reply to parent",
            parent=parent_comment
        )
        self.assertFalse(reply_comment.is_parent())
        self.assertEqual(reply_comment.parent, parent_comment)
        self.assertIn(reply_comment, parent_comment.get_replies())

    def test_comment_ordering(self):
        """Comments should be ordered by creation time."""
        first_comment = Comment.objects.create(post=self.post, user=self.user, content="First comment")
        second_comment = Comment.objects.create(post=self.post, user=self.user, content="Second comment")
        comments = Comment.objects.all()
        self.assertEqual(list(comments), [first_comment, second_comment])
