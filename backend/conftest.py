"""Shared PyTest fixtures for all apps."""
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.bookings.models import AvailabilitySlot, Booking
from apps.courses.models import Course, Subject


def make_user(username, role):
    return get_user_model().objects.create_user(
        username=username, email=f"{username}@example.com", password="pass12345", role=role
    )


@pytest.fixture
def student():
    return make_user("student1", "student")


@pytest.fixture
def other_student():
    return make_user("student2", "student")


@pytest.fixture
def educator():
    return make_user("educator1", "educator")


@pytest.fixture
def tutor():
    return make_user("tutor1", "tutor")


@pytest.fixture
def subject():
    return Subject.objects.create(slug="math", name_en="Mathematics", name_uz="Matematika")


@pytest.fixture
def course(educator, subject):
    return Course.objects.create(
        educator=educator, subject=subject, title="Algebra 1",
        level="beginner", language="en", price="10.00",
    )


@pytest.fixture
def slot(tutor):
    start = timezone.now() + timedelta(days=1)
    return AvailabilitySlot.objects.create(
        host=tutor, starts_at=start, ends_at=start + timedelta(hours=1), price="15.00"
    )


@pytest.fixture
def booking(slot, student):
    return Booking.objects.create(
        slot=slot, student=student, booking_type="tutor_lesson", status="completed", price=slot.price
    )
