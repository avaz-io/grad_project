from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.bookings.models import AvailabilitySlot, Booking, Review


def book(slot, student, status="pending"):
    return Booking.objects.create(
        slot=slot, student=student, booking_type="tutor_lesson", status=status, price=slot.price
    )


# ---------- no double-booking ----------

@pytest.mark.django_db
def test_slot_cannot_have_two_active_bookings(slot, student, other_student):
    book(slot, student)

    with pytest.raises(IntegrityError), transaction.atomic():
        book(slot, other_student)

    assert slot.bookings.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize("first_status", ["awaiting_payment", "pending", "confirmed", "completed"])
def test_every_active_status_blocks_the_slot(slot, student, other_student, first_status):
    book(slot, student, status=first_status)

    with pytest.raises(IntegrityError), transaction.atomic():
        book(slot, other_student)


@pytest.mark.django_db
@pytest.mark.parametrize("first_status", ["cancelled", "declined"])
def test_cancelled_or_declined_booking_frees_the_slot(slot, student, other_student, first_status):
    book(slot, student, status=first_status)

    second = book(slot, other_student)

    assert second.pk is not None
    assert slot.bookings.count() == 2


@pytest.mark.django_db
def test_slot_must_end_after_it_starts(tutor, slot):
    with pytest.raises(IntegrityError), transaction.atomic():
        AvailabilitySlot.objects.create(
            host=tutor, starts_at=slot.starts_at, ends_at=slot.starts_at - timedelta(minutes=30)
        )


# ---------- review rating 1-5 ----------

@pytest.mark.django_db
@pytest.mark.parametrize("rating", [1, 3, 5])
def test_review_accepts_ratings_1_to_5(booking, rating):
    review = Review(booking=booking, rating=rating)
    review.full_clean()  # model validation (used by admin and forms)
    review.save()

    assert Review.objects.get(pk=review.pk).rating == rating


@pytest.mark.django_db
@pytest.mark.parametrize("rating", [0, 6])
def test_review_validation_rejects_rating_outside_1_to_5(booking, rating):
    with pytest.raises(ValidationError) as error:
        Review(booking=booking, rating=rating).full_clean()

    assert "rating" in error.value.message_dict


@pytest.mark.django_db
@pytest.mark.parametrize("rating", [0, 6])
def test_database_rejects_rating_outside_1_to_5(booking, rating):
    # Even if validation is skipped, the database check constraint stops bad data.
    with pytest.raises(IntegrityError), transaction.atomic():
        Review.objects.create(booking=booking, rating=rating)


@pytest.mark.django_db
def test_only_one_review_per_booking(booking):
    Review.objects.create(booking=booking, rating=5)

    with pytest.raises(IntegrityError), transaction.atomic():
        Review.objects.create(booking=booking, rating=4)
