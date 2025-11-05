import pytest
from django.utils.text import slugify
from blogs.models import Category


@pytest.mark.django_db
class TestCategoryModel:
    """Test suite for the Category model."""

    def test_category_str_returns_name(self):
        """__str__ method should return the category name."""
        category = Category.objects.create(name="Technology")
        assert str(category) == "Technology"

    def test_slug_is_generated_automatically(self):
        """Slug should be generated automatically from the name if not provided."""
        category = Category.objects.create(name="Machine Learning")
        expected_slug = slugify("Machine Learning")

        assert category.slug == expected_slug
        assert category.slug == "machine-learning"

    def test_slug_is_not_overwritten_if_provided(self):
        """If slug is manually provided, it should remain unchanged."""
        category = Category.objects.create(name="Travel", slug="custom-slug")
        assert category.slug == "custom-slug"

    def test_categories_are_ordered_by_name(self):
        """Categories should be ordered alphabetically by name."""
        Category.objects.create(name="Zebra")
        Category.objects.create(name="Alpha")
        Category.objects.create(name="Middle")

        categories = Category.objects.all()
        names = [c.name for c in categories]

        assert names == sorted(names)
