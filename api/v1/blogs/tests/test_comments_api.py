from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from blogs.models import Comment, Post
from accounts.models import AuthorProfile

User = get_user_model()


class CommentAPITests(APITestCase):
    """Integration tests for the Comment API (class-based style)."""

    def setUp(self):
        """Create reusable test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="user1", password="testpass123", email="test@test.com")
        self.other_user = User.objects.create_user(username="user2", password="testpass123", email="test2@test2.com")

        # Manually create author profiles
        self.author_profile = AuthorProfile.objects.create(user=self.user)
        self.other_author_profile = AuthorProfile.objects.create(user=self.other_user)

        self.post = Post.objects.create(title="Test Post", content="Post content", author=self.author_profile)

        self.comment = Comment.objects.create(
            post=self.post, user=self.user, content="Initial comment"
        )

        self.list_create_url = reverse("comment-list-create", kwargs={"post_id": self.post.id})
        self.detail_url = reverse("comment-detail", kwargs={"pk": self.comment.id})

    def test_list_comments(self):
        """Ensure comments for a post are listed correctly."""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["content"], "Initial comment")

    def test_create_comment_authenticated(self):
        """Authenticated users should be able to create comments."""
        self.client.force_authenticate(user=self.user)
        payload = {"content": "This is a new comment"}
        response = self.client.post(self.list_create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.last().content, "This is a new comment")

    def test_create_comment_unauthenticated(self):
        """Unauthenticated users cannot create comments."""
        payload = {"content": "Unauthorized comment"}
        response = self.client.post(self.list_create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_update_comment_owner_only(self):
        """Only the comment owner can update their comment."""
        # Other user tries to update
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(self.detail_url, {"content": "Hacked!"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Owner updates
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, {"content": "Updated content"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "Updated content")

    def test_delete_comment_owner_only(self):
        """Only the owner or admin can delete a comment."""
        # Other user tries to delete
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)

        # Owner deletes successfully
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
