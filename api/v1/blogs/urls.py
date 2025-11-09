from django.urls import path
from .views import (
    CategoryListCreateView, 
    CategoryRetrieveUpdateDestroyView,
    PostListCreateView,
    PostDetailView,
    CommentListCreateView, 
    CommentDetailView
    )

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<slug:slug>/", CategoryRetrieveUpdateDestroyView.as_view(), name="category-detail"),
    # List all posts or create a new one
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    # Retrieve, update, or delete a specific post by its slug
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    # List all comments for a specific post or create a new one
    path("posts/<int:post_id>/comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    # Retrieve, update, or delete a specific comment by its ID
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
]
