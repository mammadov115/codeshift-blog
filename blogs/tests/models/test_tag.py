import pytest
from django.utils.text import slugify
from blogs.models import Tag


@pytest.mark.django_db
class TestTagModel:
    """Test suite for the Tag model."""

    def test_tag_str_returns_name(self):
        """__str__ method should return the tag name."""
        tag = Tag.objects.create(name="Python")
        assert str(tag) == "Python"

    def test_slug_is_generated_automatically(self):
        """Slug should be generated automatically from the tag name."""
        tag = Tag.objects.create(name="Web Development")
        expected_slug = slugify("Web Development")

        assert tag.slug == expected_slug
        assert tag.slug == "web-development"

    def test_slug_is_not_overwritten_if_provided(self):
        """If slug is manually provided, it should not be auto-generated."""
        tag = Tag.objects.create(name="Django", slug="custom-slug")
        assert tag.slug == "custom-slug"

    def test_tags_are_ordered_by_name(self):
        """Tags should be ordered alphabetically by name as defined in Meta.ordering."""
        Tag.objects.create(name="Zebra")
        Tag.objects.create(name="Alpha")
        Tag.objects.create(name="Middle")

        tags = Tag.objects.all()
        names = [t.name for t in tags]

        assert names == sorted(names)
