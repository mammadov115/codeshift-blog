from rest_framework import serializers
from blogs.models import Category, Post
from api.v1.accounts.serializers import AuthorProfileSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Automatically handles slug field as read-only for front-end.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    Provides nested category and author details for better API readability.
    """

    author = AuthorProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    # Use SlugRelatedField for write operations
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "cover_image",
            "status",
            "category",
            "category_id",
            "author",
            "views_count",
            "created_at",
            "updated_at",
            "published_at",
        ]
        read_only_fields = ["slug", "views_count", "published_at", "created_at", "updated_at"]

    def create(self, validated_data):
        """
        Automatically assign the current authenticated user's author profile
        as the post author when creating a new post.
        """
        request = self.context.get("request")
        author = getattr(request.user, "authorprofile", None)

        if not author:
            raise serializers.ValidationError(
                {"detail": "Only users with an author profile can create posts."}
            )

        validated_data["author"] = author
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Handle safe updates — prevent changing slug or author directly.
        """
        validated_data.pop("author", None)
        validated_data.pop("slug", None)
        return super().update(instance, validated_data)