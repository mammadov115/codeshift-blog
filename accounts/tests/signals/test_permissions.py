import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save

from accounts.signals import assign_group_permissions

User = get_user_model()


@pytest.mark.django_db
class TestAssignGroupPermissions:
    def test_reader_user_added_to_reader_group(self):
        """
        Ensure that when a user with role='reader' is created,
        they are automatically added to the 'Reader' group.
        """
        user = User.objects.create_user(username="reader1",email="admin@email.com", password="test123", role="reader")

        group = Group.objects.get(name="Reader")
        assert group in user.groups.all(), "Reader user must be added to Reader group."

    def test_author_user_added_to_author_group(self):
        """
        Ensure that when a user with role='author' is created,
        they are automatically added to the 'Author' group.
        """
        user = User.objects.create_user(username="author1", password="test123", role="author")

        group = Group.objects.get(name="Author")
        assert group in user.groups.all(), "Author user must be added to Author group."

    def test_user_without_role_is_not_assigned_any_group(self):
        """
        Ensure that if a user has no 'role' field or value,
        no group is assigned automatically.
        """
        user = User.objects.create_user(username="norole", password="test123")

        assert user.groups.count() == 0, "User without role should not be added to any group."
