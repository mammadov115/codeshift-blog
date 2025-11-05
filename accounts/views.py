from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render

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


def profile(request):
    return render(request, "profile.html")