from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for blog categories.
    Categories are used to group related posts (e.g., Tech, Travel, etc.).
    """
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for tags.
    Tags are used for flexible post labeling and filtering.
    """
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


class CommentInline(admin.TabularInline):
    """
    Inline view for comments under a post.
    Useful for quickly reviewing comments while editing a post.
    """
    model = Comment
    extra = 0
    fields = ("user", "content", "parent", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for blog posts.
    Provides filtering, search, and inline comment management.
    """
    list_display = ("title", "author", "status", "category", "views_count")
    list_filter = ("status", "category", "tags", "created_at")
    search_fields = ("title", "content", "author__user__username")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author", "category", "tags")
    inlines = [CommentInline]
    readonly_fields = ("views_count", "published_at" , "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Post Info", {"fields": ("title", "slug", "author", "status", "category", "tags")}),
        ("Content", {"fields": ("content", "cover_image")}),
        ("Statistics", {"fields": ("views_count", )}),
        ("Timestamps", {"fields": ("created_at", "published_at")}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for user comments.
    Handles both top-level and nested comments.
    """
    list_display = ("user", "post", "parent", "created_at", "short_content")
    list_filter = ("created_at",)
    search_fields = ("user__username", "content", "post__title")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("created_at",)

    def short_content(self, obj):
        """Display a short preview of comment content."""
        return (obj.content[:50] + "...") if len(obj.content) > 50 else obj.content

    short_content.short_description = "Content Preview"
