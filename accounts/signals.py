from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def assign_group_permissions(sender, instance, created, **kwargs):
    """
    Automatically assign groups and permissions based on user type.
    """

    if not created:
        return

    # Example: your user model has a field like 'role' = ['reader', 'author']
    if hasattr(instance, "role"):
        role = instance.role.lower()
        print(role)
    else:
        role = None

    if role == "reader":
        group, _ = Group.objects.get_or_create(name="Reader")
    elif role == "author":
        group, _ = Group.objects.get_or_create(name="Author")
    else:
        return

    # Attach group to user
    instance.groups.add(group)
