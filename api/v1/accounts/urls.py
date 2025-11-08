from django.urls import path
from .views import (RegisterView, 
                    LoginView, 
                    AuthorProfileListView, 
                    AuthorProfileRetrieveUpdateView,
                    ReaderProfileListView, 
                    ReaderProfileRetrieveUpdateView
)


urlpatterns = [
    # User authentication and registration endpoints
    path("register/", RegisterView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
    # List all authors (read-only)
    path("authors/", AuthorProfileListView.as_view(), name="author-list"),
    # Retrieve or update a specific author's profile
    path("authors/<int:id>/", AuthorProfileRetrieveUpdateView.as_view(), name="author-detail"),
     # List all readers (read-only)
    path("readers/", ReaderProfileListView.as_view(), name="reader-list"),
    # Retrieve or update a specific reader's profile
    path("readers/<int:id>/", ReaderProfileRetrieveUpdateView.as_view(), name="reader-detail"),
]
