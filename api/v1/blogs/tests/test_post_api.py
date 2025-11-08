from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from blogs.models import Post, Category, AuthorProfile
from accounts.models import User


class PostAPITests(APITestCase):
    """
    Test suite for Post API endpoints, including create, list, retrieve,
    update, and delete operations.
    """

    def setUp(self):
        """
        Initialize test data and authentication tokens.
        """
        self.category = Category.objects.create(name="Technology")

        # Create users
        self.author_user = User.objects.create_user(
            username="author_user",
            email="author@example.com",
            password="AuthorPass123",
            role="author",
        )
        self.reader_user = User.objects.create_user(
            username="reader_user",
            email="reader@example.com",
            password="ReaderPass123",
            role="reader",
        )

        # Create author profile
        self.author_profile = AuthorProfile.objects.create(user=self.author_user)

        # Generate JWT tokens
        self.author_token = str(RefreshToken.for_user(self.author_user).access_token)
        self.reader_token = str(RefreshToken.for_user(self.reader_user).access_token)

        # URLs
        self.post_list_url = reverse("post-list-create")

        # Create one sample post
        self.post = Post.objects.create(
            author=self.author_profile,
            title="Sample Post",
            content="This is a sample post content.",
            status=Post.Status.PUBLISHED,
            category=self.category,
        )
        self.post_detail_url = reverse("post-detail", kwargs={"slug": self.post.slug})


    def test_list_posts(self):
        """
        Ensure that all published posts are listed successfully.
        """
        response = self.client.get(self.post_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn("Sample Post", response.data[0]["title"])

    def test_create_post_as_author(self):
        """
        Verify that an authenticated author can create a post.
        """
        data = {
            "title": "New Tech Post",
            "content": "Content about technology.",
            "status": "draft",
            "category": self.category.id,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.author_token}")
        
        response = self.client.post(self.post_list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(response.data["title"], "New Tech Post")

    def test_create_post_as_reader_forbidden(self):
        """
        Ensure that readers cannot create posts.
        """
        data = {
            "title": "Reader Attempt",
            "content": "Trying to post as a reader.",
            "status": "draft",
            "category": self.category.id,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.reader_token}")
        response = self.client.post(self.post_list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)

    def test_retrieve_post_detail(self):
        """
        Ensure that a post can be retrieved by slug.
        """
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], self.post.slug)
        self.assertEqual(response.data["title"], self.post.title)

    def test_update_post_by_author(self):
        """
        Verify that an author can update their own post.
        """
        updated_data = {"title": "Updated Sample Post"}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.author_token}")
        response = self.client.patch(self.post_detail_url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Sample Post")

    def test_delete_post_by_author(self):
        """
        Ensure an author can delete their own post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.author_token}")
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(slug=self.post.slug).exists())

    def test_reader_cannot_delete_post(self):
        """
        Ensure that a reader cannot delete an author's post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.reader_token}")
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(slug=self.post.slug).exists())
