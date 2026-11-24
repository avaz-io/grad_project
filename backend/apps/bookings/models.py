from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q

from apps.courses.models import ContentLanguage, Level, Subject
from apps.integrations.choices import ZoomStatus


class VerificationStatus(models.TextChoices):
    """Admin verification of tutors and mentors. Unverified profiles are not ranked."""

    PENDING = "pending", "Pending"
    VERIFIED = "verified", "Verified"
    REJECTED = "rejected", "Rejected"


def _languages_field():
    """List of language codes, e.g. ["en", "uz"]. Stored as a PostgreSQL array."""
    return ArrayField(
        models.CharField(max_length=2, choices=ContentLanguage.choices), default=list, blank=True
    )


class TutorProfile(models.Model):
    """A tutor's public profile. Rating fields are a cache updated when a review is saved."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="tutor_profile",
    )
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    languages = _languages_field()
    verification_status = models.CharField(
        max_length=10, choices=VerificationStatus.choices, default=VerificationStatus.PENDING
    )
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)

    # Many-to-many: tutors <-> subjects, stored in the TutorSubject table.
    subjects = models.ManyToManyField(Subject, through="TutorSubject", related_name="tutors")

    def __str__(self):
        return f"Tutor {self.user}"


class TutorSubject(models.Model):
    """A subject a tutor teaches, with the range of levels they teach it at."""

    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name="tutor_subjects")
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="tutor_subjects")
    min_level = models.CharField(max_length=20, choices=Level.choices)
    max_level = models.CharField(max_length=20, choices=Level.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tutor", "subject"], name="unique_tutor_subject"),
        ]

    def __str__(self):
        return f"{self.tutor} - {self.subject}"


class MentorProfile(models.Model):
    """A mentor's public profile for advice and consulting sessions."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="mentor_profile",
    )
    bio = models.TextField(blank=True)
    topics = models.CharField(max_length=255, blank=True, help_text="e.g. career, university applications")
    default_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="0 = free")
    languages = _languages_field()
    verification_status = models.CharField(
        max_length=10, choices=VerificationStatus.choices, default=VerificationStatus.PENDING
    )
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Mentor {self.user}"


class AvailabilitySlot(models.Model):
    """One bookable time block offered by a tutor or a mentor."""

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="availability_slots",
        limit_choices_to={"role__in": ["tutor", "mentor"]},
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="0 = free")
    is_active = models.BooleanField(default=True, help_text="Untick to withdraw an unbooked slot.")

    class Meta:
        ordering = ["starts_at"]
        constraints = [
            models.CheckConstraint(condition=Q(ends_at__gt=F("starts_at")), name="slot_ends_after_start"),
            models.CheckConstraint(condition=Q(price__gte=0), name="slot_price_not_negative"),
        ]

    def __str__(self):
        return f"{self.host} {self.starts_at:%Y-%m-%d %H:%M}"


# Bookings in these statuses hold the slot. Declined/cancelled ones free it again.
# (Defined at module level so Booking.Meta below can use it.)
ACTIVE_BOOKING_STATUSES = ["awaiting_payment", "pending", "confirmed", "completed"]


class Booking(models.Model):
    """A student's booking of a slot: a tutor lesson or a mentor consultation."""

    class BookingType(models.TextChoices):
        TUTOR_LESSON = "tutor_lesson", "Tutor lesson"
        MENTOR_CONSULTATION = "mentor_consultation", "Mentor consultation"

    class Status(models.TextChoices):
        AWAITING_PAYMENT = "awaiting_payment", "Awaiting payment"
        PENDING = "pending", "Waiting for host"
        CONFIRMED = "confirmed", "Confirmed"
        DECLINED = "declined", "Declined"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    slot = models.ForeignKey(AvailabilitySlot, on_delete=models.PROTECT, related_name="bookings")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, null=True, blank=True, related_name="bookings",
        help_text="Tutor lessons only.",
    )
    booking_type = models.CharField(max_length=20, choices=BookingType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, help_text="Copied from the slot when booked."
    )
    student_note = models.TextField(blank=True)
    zoom_meeting_id = models.CharField(max_length=50, blank=True)
    zoom_link = models.URLField(max_length=500, blank=True)
    zoom_status = models.CharField(
        max_length=10, choices=ZoomStatus.choices, default=ZoomStatus.NONE
    )
    cancelled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",  # no reverse accessor needed
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # No double-booking: at most one active booking per slot.
            # It is a partial unique index, so cancelled bookings don't block the slot.
            models.UniqueConstraint(
                fields=["slot"],
                condition=Q(status__in=ACTIVE_BOOKING_STATUSES),
                name="one_active_booking_per_slot",
            ),
            models.CheckConstraint(condition=Q(price__gte=0), name="booking_price_not_negative"),
        ]

    def __str__(self):
        return f"{self.student} booked {self.slot}"


class Review(models.Model):
    """A rating (1-5) and comment for a completed booking. One review per booking."""

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="review")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Validators catch bad input in forms/API; this also protects the database itself.
            models.CheckConstraint(condition=Q(rating__gte=1, rating__lte=5), name="review_rating_1_to_5"),
        ]

    def __str__(self):
        return f"{self.rating}/5 for booking {self.booking_id}"
