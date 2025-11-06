from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()


class UserRegisterViewTests(TestCase):
    """
    Test suite for UserRegisterView.
    Covers valid registration, invalid form submission, and message handling.
    """

    def setUp(self):
        """Initialize test data and URLs."""
        self.signup_url = reverse("signup")
        self.home_url = reverse("home")

    def test_signup_page_renders_correct_template(self):
        """Ensure the signup page renders successfully."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

    def test_valid_user_registration_creates_account(self):
        """Ensure a valid registration creates a user and redirects to home."""
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        response = self.client.post(self.signup_url, form_data, follow=True)

        # Check user creation
        self.assertTrue(User.objects.filter(username="newuser").exists())

        # Check redirect to home
        self.assertRedirects(response, self.home_url)

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Your account has been created successfully" in str(msg) for msg in messages))

        # Check if the user is logged in
        user = response.context["user"]
        self.assertTrue(user.is_authenticated)

    def test_invalid_registration_shows_error_messages(self):
        """Ensure invalid form submission shows error messages."""
        form_data = {
            "username": "",  # Missing username
            "email": "invalidemail",  # Invalid email
            "password1": "pass123",
            "password2": "differentpass",
        }

        response = self.client.post(self.signup_url, form_data, follow=True)

        # Should not create user
        self.assertFalse(User.objects.exists())

        # Should render the same signup page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

        # Should contain error messages
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Registration failed" in str(msg) for msg in messages))
        self.assertTrue(any("Password" in str(msg) or "Email" in str(msg) for msg in messages))
