from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from accounts.models import AuthorProfile, ReaderProfile

from .permissions import IsAnonymousUser, IsAuthorUser, IsReaderUser
from .serializers import (RegisterSerializer, 
                          LoginSerializer, 
                          AuthorProfileSerializer, 
                          ReaderProfileSerializer
                          )



User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for registering new users.
    Automatically creates AuthorProfile or ReaderProfile based on role.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymousUser]

    def create(self, request, *args, **kwargs):
        """
        Override create() to customize response and create related profile.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create related profile based on role
        if user.role == "author":
            AuthorProfile.objects.create(user=user)
        elif user.role == "reader":
            ReaderProfile.objects.create(user=user)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": "User registered successfully.",
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class LoginView(generics.GenericAPIView):
    """
    Generic API view for user login with JWT tokens.
    Only anonymous users can access this endpoint.
    """

    serializer_class = LoginSerializer
    permission_classes = [IsAnonymousUser]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to authenticate user and return JWT tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        return Response({
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_author": user.is_author,
            "is_reader": user.is_reader,
            "profile_image": user.get_profile_image,
            "access": serializer.validated_data["access"],
            "refresh": serializer.validated_data["refresh"],
        }, status=status.HTTP_200_OK)


class AuthorProfileListView(generics.ListAPIView):
    """
    List all authors. Read-only endpoint.
    """
    queryset = AuthorProfile.objects.all()
    serializer_class = AuthorProfileSerializer
    permission_classes = [IsAuthenticated]


class AuthorProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the author's own profile.
    Only the profile owner can update it.
    """
    queryset = AuthorProfile.objects.all()
    serializer_class = AuthorProfileSerializer
    permission_classes = [IsAuthenticated, IsAuthorUser]
    lookup_field = "id"


class ReaderProfileListView(generics.ListAPIView):
    """
    List all readers. Read-only endpoint.
    """
    queryset = ReaderProfile.objects.all()
    serializer_class = ReaderProfileSerializer
    permission_classes = [IsAuthenticated]


class ReaderProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the reader's own profile.
    Only the profile owner can update it.
    """
    queryset = ReaderProfile.objects.all()
    serializer_class = ReaderProfileSerializer
    permission_classes = [IsAuthenticated, IsReaderUser]
    lookup_field = "id"