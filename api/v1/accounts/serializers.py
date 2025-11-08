from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.

    Handles validation, password hashing, and user creation.
    Supports both 'author' and 'reader' roles.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )

    confirm_password = serializers.CharField(
        write_only=True,
        help_text="Must match the password field."
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
            "role",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "role": {"required": True},
        }

    def validate_email(self, value):
        """
        Ensure email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        """
        Ensure both password fields match.
        """
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Create a new user with a hashed password.
        """
        validated_data.pop("confirm_password")  # Not needed for creation
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
