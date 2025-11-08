from rest_framework import generics
from blogs.models import Category, Post
from .serializers import CategorySerializer, PostSerializer
from .permissions import IsAdminOrReadOnly, IsVerifiedAuthor, IsAuthorOrReadOnly
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