from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model.
    Ensures email is required and supports create_user & create_superuser methods.
    """

    def create_user(self, username, email, password=None, **extra_fields):
        """Create and return a regular user with a unique email."""
        if not email:
            raise ValueError("The Email field is required.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and return a superuser with elevated permissions."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not password:
            raise ValueError("Superusers must have a password.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Base user model that handles authentication and shared user info.
    Separate profile models (AuthorProfile, ReaderProfile) extend this base.
    """

    ROLE_CHOICES = [
        ("author", "Author"),
        ("reader", "Reader"),
    ]

    # Common fields for all users
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # User type (role)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="reader",
        help_text="Defines the user's role: Author or Reader."
    )

    # Attach the custom manager
    objects = CustomUserManager()

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
    
    @property
    def get_profile_image(self):
        """Return user's profile image URL, regardless of whether they're author or reader."""
        if hasattr(self, "authorprofile") and self.authorprofile.profile_image:
            return self.authorprofile.profile_image.url
        elif hasattr(self, "readerprofile") and getattr(self.readerprofile, "profile_image", None):
            return self.readerprofile.profile_image.url
        return "/static/images/default_profile.png"  # fallback image


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
    profile_image = models.ImageField(upload_to="readers/", blank=True, null=True)

    def __str__(self):
        return f"Reader: {self.user.username}"


