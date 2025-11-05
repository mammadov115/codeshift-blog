from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from accounts.models import AuthorProfile
from .category import Category
from .tag import Tag

class Article(models.Model):
    """Core blog post model representing an article."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    author = models.ForeignKey(
        AuthorProfile,
        on_delete=models.CASCADE,
        related_name="posts",
        help_text="Author who wrote the post."
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to="post_covers/", blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Post status: Draft or Published."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    views_count = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug and published_at timestamp."""
        if not self.slug:
            self.slug = slugify(self.title)

        # Set publish date when status changes to published
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def increment_views(self):
        """Increase the view count each time the post is viewed."""
        self.views_count = models.F("views_count") + 1
        self.save(update_fields=["views_count"])

    def total_reactions(self):
        """Returns total number of likes and dislikes."""
        return self.likes + self.dislikes