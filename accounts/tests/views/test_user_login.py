from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()


class UserLoginViewTests(TestCase):
    """
    Test suite for the UserLoginView.
    Covers successful login, failed login, and redirect behavior.
    """

    def setUp(self):
        """Create a test user for authentication tests."""
        self.password = "testpassword123"
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password=self.password
        )
        self.login_url = reverse("login")
        self.home_url = reverse("home")

    def test_login_page_renders_correct_template(self):
        """Ensure the login page loads successfully with the correct template."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_valid_user_login_redirects_to_home(self):
        """Test that a user with valid credentials is successfully logged in."""
        response = self.client.post(
            self.login_url,
            {"username": self.user.username, "password": self.password},
            follow=True
        )
        self.assertRedirects(response, self.home_url)
        self.assertTrue(response.context["user"].is_authenticated)

        # Check that a success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Welcome back" in str(msg) for msg in messages))

    def test_invalid_user_login_shows_error(self):
        """Test that invalid credentials return an error message."""
        response = self.client.post(
            self.login_url,
            {"username": self.user.username, "password": "wrongpassword"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)

        # Check that an error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Invalid username or password" in str(msg) for msg in messages))

    def test_authenticated_user_redirects_from_login(self):
        """Test that an already logged-in user is redirected away from the login page."""
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(self.login_url, follow=True)
        self.assertRedirects(response, self.home_url)
