import pytest
from django.utils.text import slugify
from django.utils import timezone
from blogs.models import Post, Category, Tag
from accounts.models import AuthorProfile


@pytest.mark.django_db
class TestPostModel:
    """Test suite for the Post model."""

    @pytest.fixture
    def author(self, django_user_model):
        """Create a sample author for testing."""
        user = django_user_model.objects.create_user(
            username="author_user", email="author@example.com", password="testpass123"
        )
        return AuthorProfile.objects.create(user=user, bio="Tech writer")

    @pytest.fixture
    def category(self):
        """Create a sample category for posts."""
        return Category.objects.create(name="Technology")

    def test_slug_is_generated_automatically(self, author, category):
        """Slug should be automatically created from the title."""
        post = Post.objects.create(
            author=author,
            title="My First Django Post",
            content="Sample content",
            category=category,
        )
        expected_slug = slugify("My First Django Post")

        assert post.slug == expected_slug
        assert post.slug == "my-first-django-post"

    def test_published_at_is_set_when_status_published(self, author, category):
        """When post is published, published_at should be automatically set."""
        post = Post.objects.create(
            author=author,
            title="Published Post",
            content="Some text",
            category=category,
            status=Post.Status.PUBLISHED,
        )

        assert post.published_at is not None
        assert isinstance(post.published_at, timezone.datetime)

    def test_increment_views_increases_count(self, author, category):
        """increment_views() should correctly increase view count."""
        post = Post.objects.create(
            author=author,
            title="View Counter Post",
            content="Some content",
            category=category,
        )

        initial_views = post.views_count
        post.increment_views()
        post.refresh_from_db()

        assert post.views_count == initial_views + 1

    def test_total_reactions_returns_sum(self, author, category):
        """total_reactions() should return sum of likes and dislikes."""
        post = Post.objects.create(
            author=author,
            title="Reaction Post",
            content="Testing likes/dislikes",
            category=category,
            likes=15,
            dislikes=5,
        )
        assert post.total_reactions() == 20

    def test_default_values_are_zero(self, author, category):
        """New post should have 0 likes, dislikes, and views by default."""
        post = Post.objects.create(
            author=author,
            title="Default Values Post",
            content="Content",
            category=category,
        )

        assert post.likes == 0
        assert post.dislikes == 0
        assert post.views_count == 0
