from rest_framework import serializers
from blogs.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Automatically handles slug field as read-only for front-end.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]
