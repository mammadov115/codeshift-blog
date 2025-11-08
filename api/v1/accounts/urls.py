from django.urls import path
from .views import RegisterView


urlpatterns = [
    # User authentication and registration endpoints
    path("register/", RegisterView.as_view(), name="user-register"),


]
