from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("signup/", views.UserRegisterView.as_view(), name="signup"),
    path("profile/", views.UserProfileView.as_view(), name="profile")

]
