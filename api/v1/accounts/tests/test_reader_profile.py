from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from accounts.models import ReaderProfile

User = get_user_model()


class ReaderProfileAPITests(APITestCase):
    """
    Test suite for ReaderProfile API endpoints.
    """

    def setUp(self):
        """
        Create test users and reader profiles.
        """
        # Reader 1
        self.reader1 = User.objects.create_user(
            username="reader1", email="reader1@example.com", password="Pass1234", role="reader"
        )
        self.profile1 = ReaderProfile.objects.create(user=self.reader1, subscribed=True)

        # Reader 2
        self.reader2 = User.objects.create_user(
            username="reader2", email="reader2@example.com", password="Pass1234", role="reader"
        )
        self.profile2 = ReaderProfile.objects.create(user=self.reader2, subscribed=False)

        self.list_url = reverse("reader-list")
        self.detail_url1 = reverse("reader-detail", kwargs={"id": self.profile1.id})
        self.detail_url2 = reverse("reader-detail", kwargs={"id": self.profile2.id})

    def test_reader_list_authenticated(self):
        self.client.force_authenticate(user=self.reader1)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_reader_list_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_own_profile(self):
        self.client.force_authenticate(user=self.reader1)
        response = self.client.get(self.detail_url1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["subscribed"], self.profile1.subscribed)

    def test_retrieve_other_profile(self):
        self.client.force_authenticate(user=self.reader1)
        response = self.client.get(self.detail_url2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["subscribed"], self.profile2.subscribed)

    def test_update_own_profile(self):
        self.client.force_authenticate(user=self.reader1)
        payload = {"subscribed": False}
        response = self.client.put(self.detail_url1, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile1.refresh_from_db()
        self.assertEqual(self.profile1.subscribed, False)

    def test_update_other_profile_forbidden(self):
        self.client.force_authenticate(user=self.reader1)
        payload = {"subscribed": True}
        response = self.client.put(self.detail_url2, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_unauthenticated_forbidden(self):
        payload = {"subscribed": True}
        response = self.client.put(self.detail_url1, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
