from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import AuthorProfile, ReaderProfile

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


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login using username and password.
    Returns JWT tokens if authentication is successful.
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True
    )

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    user_id = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        """
        Validate user credentials and generate JWT tokens.
        """
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Username and password are required.")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)
        attrs["user"] = user  # optional, if you want user info in view
        attrs["user_id"] = user.id

        return attrs


class AuthorProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for AuthorProfile model.
    Includes nested user info and handles read-only fields like total_posts.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    profile_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AuthorProfile
        fields = [
            "id",
            "username",
            "email",
            "role",
            "bio",
            "website",
            "profile_image",
            "profile_image_url",
            "verified",
            "total_posts",
        ]
        read_only_fields = ["id", "username", "email", "role", "total_posts", "profile_image_url"]

    def get_profile_image_url(self, obj):
        """
        Return the full URL of the author's profile image or a default image.
        """
        request = self.context.get("request")
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url) if request else obj.profile_image.url
        return "/static/images/default_profile.png"


class ReaderProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for ReaderProfile model.
    Includes nested user info and full profile image URL.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    profile_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReaderProfile
        fields = [
            "id",
            "username",
            "email",
            "role",
            "subscribed",
            "profile_image",
            "profile_image_url",
        ]
        read_only_fields = ["id", "username", "email", "role", "profile_image_url"]

    def get_profile_image_url(self, obj):
        """
        Return full URL of the reader's profile image, or default if not provided.
        """
        request = self.context.get("request")
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url) if request else obj.profile_image.url
        return "/static/images/default_profile.png"