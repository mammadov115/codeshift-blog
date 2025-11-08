from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from .permissions import IsAnonymousUser

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for registering new users using Django REST Framework's generic view.
    Provides built-in request handling and serializer validation.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymousUser]

    def create(self, request, *args, **kwargs):
        """
        Override create() to customize the response format.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

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
