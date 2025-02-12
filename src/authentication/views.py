from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import CustomUser
from .serializers import CustomUserCreateSerializer, CustomUserListSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `create`, `retrieve`, `update`, `partial_update`, `destroy`, and `list` actions.
    The `create` action is accessible to unauthenticated users, while all other actions require authentication.

    Methods:
        get_permissions():
            Allows unauthenticated users to access the `create` action, while all other actions require authentication.
        get_queryset():
            Returns the queryset of CustomUser instances for the currently authenticated user based on the action.
        get_serializer_class():
            Returns the appropriate serializer class based on the action to does not expose sensitive data to other users.
    """

    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return CustomUser.objects.filter(id=self.request.user.id)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return CustomUserCreateSerializer
        else:
            return CustomUserListSerializer
