from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.bookings.models import Booking
from apps.courses.models import Enrollment


class Payment(models.Model):
    """One payment attempt for a course enrolment or a paid session (test mode only).

    Links use PROTECT so payment history can't be deleted by accident.
    """

    class Provider(models.TextChoices):
        STRIPE = "stripe", "Stripe (test mode)"
        FAKE = "fake", "Fake payment service"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="payments"
    )
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.PROTECT, null=True, blank=True, related_name="payments"
    )
    booking = models.ForeignKey(
        Booking, on_delete=models.PROTECT, null=True, blank=True, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    provider = models.CharField(max_length=10, choices=Provider.choices)
    provider_payment_id = models.CharField(
        max_length=100, blank=True, help_text="e.g. Stripe PaymentIntent id"
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # A payment is for exactly one thing: an enrolment or a booking.
            models.CheckConstraint(
                condition=(
                    Q(enrollment__isnull=False, booking__isnull=True)
                    | Q(enrollment__isnull=True, booking__isnull=False)
                ),
                name="payment_has_exactly_one_target",
            ),
            models.CheckConstraint(condition=Q(amount__gt=0), name="payment_amount_positive"),
        ]

    def __str__(self):
        return f"{self.amount} {self.currency} by {self.user} ({self.status})"
