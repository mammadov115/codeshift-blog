from django.urls import path
from .views import RegisterView, LoginView


urlpatterns = [
    # User authentication and registration endpoints
    path("register/", RegisterView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
]
