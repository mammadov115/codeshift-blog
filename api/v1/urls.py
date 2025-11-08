from django.urls import path, include


urlpatterns = [
    path("accounts/", include("api.v1.accounts.urls")),
    path("blogs/", include("api.v1.blogs.urls")),
    
]