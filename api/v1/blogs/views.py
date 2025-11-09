from rest_framework import generics
from blogs.models import Category, Post, Comment
from .serializers import CategorySerializer, PostSerializer, CommentSerializer
from .permissions import (IsAdminOrReadOnly,
                           IsVerifiedAuthor, 
                            IsAuthorOrReadOnly,
                             IsOwnerOrAdminOrReadOnly)
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create a new one.
    Creation restricted to admin users.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a category.
    Updates/deletes restricted to admin users.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = "slug"  # Use slug in URL for better SEO/readability


class PostListCreateView(generics.ListCreateAPIView):
    """
    View for listing all published posts and creating new ones.
    Only verified authors can create posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsVerifiedAuthor | IsAuthorOrReadOnly]


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a single post.
    Only the author can modify or delete their post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    """
    Handles listing all comments for a specific post and creating new ones.
    - Anyone can read comments.
    - Authenticated users can add comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """
        Return all comments for a specific post.
        If 'post_id' is in the URL, filter by it.
        """
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id, parent=None).select_related("user", "post")

    def perform_create(self, serializer):
        """
        Automatically set the user and post when creating a comment.
        """
        post_id = self.kwargs.get("post_id")
        serializer.save(user=self.request.user, post_id=post_id)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific comment.
    - Read-only for everyone.
    - Only owner or admin can modify/delete.
    """
    queryset = Comment.objects.all().select_related("user", "post")
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    
