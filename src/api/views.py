from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from authentication.models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CustomUser instances.

    This viewset provides `create`, `retrieve`, `update`, `partial_update`, `destroy`, and `list` actions.
    The `create` action is accessible to unauthenticated users, while all other actions require authentication.

    Methods:
        get_permissions():
            Allows unauthenticated users to access the `create` action, while all other actions require authentication.
    """
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else: 
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()