from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Base user model that handles authentication and shared user info.
    Separate profile models (AuthorProfile, ReaderProfile) extend this base.
    """

    # Common fields for all users
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    @property
    def is_author(self):
        """Check if this user has an author profile."""
        return hasattr(self, "authorprofile")

    @property
    def is_reader(self):
        """Check if this user has a reader profile."""
        return hasattr(self, "readerprofile")
    

class AuthorProfile(models.Model):
    """
    Profile for blog authors.
    Extends the base User model with author-specific data.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="authorprofile"
    )
    bio = models.TextField(blank=True, help_text="Author biography.")
    website = models.URLField(blank=True, null=True, help_text="Personal website or portfolio.")
    profile_image = models.ImageField(upload_to="authors/", blank=True, null=True)
    verified = models.BooleanField(default=False, help_text="Verified author badge.")
    total_posts = models.PositiveIntegerField(default=0, help_text="Number of published posts.")

    def __str__(self):
        return f"Author: {self.user.username}"


class ReaderProfile(models.Model):
    """
    Profile for normal readers.
    Extend this if readers can do more than just reading (e.g., saving favorites).
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="readerprofile"
    )
    subscribed = models.BooleanField(default=False, help_text="Whether the user is subscribed to the newsletter.")
    favorite_posts = models.ManyToManyField(
        "blogs.Post",
        related_name="favorited_by",
        blank=True,
        help_text="Posts this reader marked as favorite."
    )

    def __str__(self):
        return f"Reader: {self.user.username}"
