from rest_framework import generics
from blogs.models import Category
from .serializers import CategorySerializer
from .permissions import IsAdminOrReadOnly
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
