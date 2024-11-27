from django.shortcuts import render
from rest_framework import viewsets

from authentication.models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
