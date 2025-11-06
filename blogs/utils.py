from django.db.models import Q
from .models import Post

def search_posts(search_query):
    if not search_query:
        return Post.objects.all()
    return Post.objects.filter(
        Q(title__icontains=search_query) |
        Q(content__icontains=search_query) |
        Q(category__name__icontains=search_query)
    ).distinct()
