from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from trip.models import Trip
from authentication.models import CustomUser


class Review(models.Model):
    """
    Attributes:
        - user (ForeignKey): The user who made the review.
        - reviewer (ForeignKey): The user who received the review.
        - trip (ForeignKey): The trip that was reviewed.
        - rating (PositiveIntegerField): The rating of the review.
        - comment (TextField): The comment of the review.

    Attributes inherits from Model:
        - id (AutoField): The primary key for the review.

    Methods:
        - __str__: Returns a string representation of the review.
        - clean: Validates that the reviewer participated in the trip.

    Meta:
        - unique_together: A user can only review a each participant of a trip once.
    """

    user = models.ForeignKey(
        CustomUser,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name="Usuario",
    )
    reviewer = models.ForeignKey(
        CustomUser,
        related_name="reviews_made",
        on_delete=models.CASCADE,
        verbose_name="Revisor",
    )
    trip = models.ForeignKey(
        Trip, related_name="reviews", on_delete=models.CASCADE, verbose_name="Viaje"
    )
    rating = models.PositiveIntegerField(
        verbose_name="Calificación",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(
        verbose_name="Comentario", null=True, blank=True, max_length=500
    )

    class Meta:
        unique_together = (
            "user",
            "trip",
            "reviewer",
        )
