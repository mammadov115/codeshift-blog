from django.urls import path
from .views import (
    CategoryListCreateView, 
    CategoryRetrieveUpdateDestroyView,
    PostListCreateView,
    PostDetailView
    )

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<slug:slug>/", CategoryRetrieveUpdateDestroyView.as_view(), name="category-detail"),
    # List all posts or create a new one
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    # Retrieve, update, or delete a specific post by its slug
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
]
