from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from blogs.models import Category

User = get_user_model()


class CategoryAPITests(APITestCase):
    """
    Test suite for Category API endpoints.
    """

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="Pass1234"
        )
        self.user = User.objects.create_user(
            username="user", email="user@example.com", password="Pass1234"
        )

        self.category = Category.objects.create(name="Tech")
        self.list_create_url = reverse("category-list-create")
        self.detail_url = reverse("category-detail", kwargs={"slug": self.category.slug})

    def test_list_categories(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_category_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Travel"}
        response = self.client.post(self.list_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name="Travel").exists())

    def test_create_category_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "Health"}
        response = self.client.post(self.list_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_category(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)

    def test_update_category_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Updated Tech"}
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Tech")

    def test_update_category_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "Should Fail"}
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_delete_category_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
