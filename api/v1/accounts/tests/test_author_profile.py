from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from accounts.models import AuthorProfile

User = get_user_model()


class AuthorProfileAPITests(APITestCase):
    """
    Test suite for AuthorProfile API endpoints.
    """

    def setUp(self):
        """
        Create test users and author profiles.
        """
        # Author 1
        self.author1 = User.objects.create_user(
            username="author1", email="author1@example.com", password="Pass1234", role="author"
        )
        self.profile1 = AuthorProfile.objects.create(
            user=self.author1,
            bio="Author 1 bio",
            website="https://author1.com",
            verified=True,
            total_posts=5
        )

        # Author 2
        self.author2 = User.objects.create_user(
            username="author2", email="author2@example.com", password="Pass1234", role="author"
        )
        self.profile2 = AuthorProfile.objects.create(
            user=self.author2,
            bio="Author 2 bio",
            website="https://author2.com",
            verified=False,
            total_posts=2
        )

        self.list_url = reverse("author-list")
        self.detail_url1 = reverse("author-detail", kwargs={"id": self.profile1.id})
        self.detail_url2 = reverse("author-detail", kwargs={"id": self.profile2.id})

    def test_author_list_authenticated(self):
        """
        Authenticated user can view list of authors.
        """
        self.client.force_authenticate(user=self.author1)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_author_list_unauthenticated(self):
        """
        Unauthenticated user cannot view list of authors.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_own_profile(self):
        """
        Author can retrieve their own profile.
        """
        self.client.force_authenticate(user=self.author1)
        response = self.client.get(self.detail_url1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], self.profile1.bio)

    def test_retrieve_other_profile(self):
        """
        Author can retrieve another author's profile (read-only).
        """
        self.client.force_authenticate(user=self.author1)
        response = self.client.get(self.detail_url2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], self.profile2.bio)

    def test_update_own_profile(self):
        """
        Author can update their own profile.
        """
        self.client.force_authenticate(user=self.author1)
        payload = {"bio": "Updated bio", "website": "https://newauthor1.com"}
        response = self.client.put(self.detail_url1, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile1.refresh_from_db()
        self.assertEqual(self.profile1.bio, payload["bio"])
        self.assertEqual(self.profile1.website, payload["website"])

    def test_update_other_profile_forbidden(self):
        """
        Author cannot update another author's profile.
        """
        self.client.force_authenticate(user=self.author1)
        payload = {"bio": "Hacked bio"}
        response = self.client.put(self.detail_url2, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_unauthenticated_forbidden(self):
        """
        Unauthenticated user cannot update any profile.
        """
        payload = {"bio": "Hacked bio"}
        response = self.client.put(self.detail_url1, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
