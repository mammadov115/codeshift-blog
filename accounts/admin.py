from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AuthorProfile, ReaderProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin configuration for the base User model.
    Adds extra fields and organizes sections for clarity.
    """

    # Fields to display in the list view
    list_display = ("username", "email", "is_staff", "is_active", "created_at", "is_author", "is_reader")
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("username", "email")
    ordering = ("-created_at",)

    # Custom field layout in the detail view
    readonly_fields = ("created_at",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields for creating a new user in admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for authors.
    Displays key author details and allows filtering by verification status.
    """

    list_display = ("user", "verified", "total_posts")
    list_filter = ("verified",)
    search_fields = ("user__username", "user__email")
    readonly_fields = ("total_posts",)
    ordering = ("-verified", "user__username")


@admin.register(ReaderProfile)
class ReaderProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for readers.
    Displays subscription status and favorite post count.
    """

    list_display = ("user", "subscribed", "favorite_count")
    list_filter = ("subscribed",)
    search_fields = ("user__username", "user__email")
    filter_horizontal = ("favorite_posts",)

    def favorite_count(self, obj):
        """Show number of favorite posts in the admin list view."""
        return obj.favorite_posts.count()

    favorite_count.short_description = "Favorites"
