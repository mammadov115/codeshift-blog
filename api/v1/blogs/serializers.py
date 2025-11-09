from rest_framework import serializers
from blogs.models import Category, Post, Comment
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
    

class RecursiveCommentSerializer(serializers.Serializer):
    """Recursively serialize nested replies."""
    def to_representation(self, instance):
        serializer = CommentSerializer(instance, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model with nested replies support."""

    user = serializers.StringRelatedField(read_only=True)  # Displays the username
    replies = RecursiveCommentSerializer(many=True, read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    parent_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "user",
            "content",
            "parent_id",
            "replies",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "replies", "user"]

    def create(self, validated_data):
        """
        Create a comment, assigning user and post from context.
        This ensures cleaner request payloads.
        """
        request = self.context.get("request")
        post = self.context.get("post")
        # user = request.user if request else None

        parent_id = validated_data.pop("parent_id", None)
        parent = Comment.objects.get(id=parent_id) if parent_id else None

        return Comment.objects.create(
            post=post,
            # user=user,
            parent=parent,
            **validated_data
        )
