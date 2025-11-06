from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post, AuthorProfile


@receiver(post_save, sender=Post)
def update_author_total_posts_on_save(sender, instance, created, **kwargs):
    """
    Update the author's total published post count whenever a Post is created or updated.
    This ensures `AuthorProfile.total_posts` always reflects the number of published posts.
    """
    author = instance.author

    # Count only published posts
    total_published = author.posts.filter(status=Post.Status.PUBLISHED).count()

    # Update author's total_posts
    AuthorProfile.objects.filter(pk=author.pk).update(total_posts=total_published)


@receiver(post_delete, sender=Post)
def update_author_total_posts_on_delete(sender, instance, **kwargs):
    """
    Update author's total post count when a post is deleted.
    """
    author = instance.author
    total_published = author.posts.filter(status=Post.Status.PUBLISHED).count()
    AuthorProfile.objects.filter(pk=author.pk).update(total_posts=total_published)
