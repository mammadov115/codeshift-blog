from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from accounts.models import User, AuthorProfile, ReaderProfile
from .forms import CustomUserCreationForm
from django.views.generic import CreateView

class UserLoginView(LoginView):
    """
    Handles user login using Django's built-in authentication system.
    Extends LoginView for cleaner and reusable login logic.
    """

    template_name = "login.html"  # Path to your login template
    redirect_authenticated_user = True     # Redirect if already logged in
    next_page = reverse_lazy("home")       # Default redirect after successful login

    def form_valid(self, form):
        """
        Called when the login form is valid.
        Displays a success message and logs the user in.
        """
        user = form.get_user()
        messages.success(self.request, f"Welcome back, {user.username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Called when login credentials are invalid.
        Displays an error message without crashing.
        """
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


class UserRegisterView(CreateView):
    """
    Handles user registration (sign-up).
    Uses Django's built-in UserCreationForm for validation and security.
    """

    model = User
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("home")  # Redirect after successful signup

    def form_valid(self, form):
        """
        Called when the submitted form is valid.
        Creates the user, logs them in, and displays a success message.
        """
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_staff = True
        role = form.data.get("role")  # Expecting a 'role' field in the form
        user.save()

        # Create the corresponding profile based on role
        if role == "author":
            AuthorProfile.objects.create(user=user)
        elif role == "reader":
            ReaderProfile.objects.create(user=user)
            
        login(self.request, user)
        messages.success(self.request, f"Welcome, {user.username}! Your account has been created successfully.")
        return response

    def form_invalid(self, form):
        """
        Called when form validation fails.
        Displays errors in a user-friendly way.
        """
        print(form.fields)
        messages.error(self.request, "Registration failed. Please correct the errors below.")
            # Loop through each field and its errors
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    # Non-field (global) errors
                    messages.error(self.request, f"{error}")
                else:
                    # Field-specific errors
                    messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)