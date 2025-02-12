from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .serializers import ReviewDetailSerializer, ReviewListSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `create`, `retrieve`, `update`, `partial_update`, `destroy`, and `list` actions.
    The `create` action assigns the authenticated user as the reviewer.

    Methods:
        get_queryset():
            Return the queryset of Review instances filtered by the authenticated user.
        get_serializer_class():
            Return the serializer class depending on the action.
        perform_create():
            Assign the authenticated user as the reviewer when creating a new review.
    """

    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action in ("update", "partial_update", "destroy"):
            return Review.objects.filter(reviewer=self.request.user)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return ReviewDetailSerializer
        return ReviewListSerializer

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
