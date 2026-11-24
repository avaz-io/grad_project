import pytest
from django.contrib.auth import get_user_model
from django.core.management import CommandError, call_command
from rest_framework.test import APIClient

from apps.bookings.models import AvailabilitySlot, MentorProfile, TutorProfile
from apps.courses.models import Course, Lesson, Subject
from apps.lectures.models import Lecture


def row_counts():
    models = [get_user_model(), Subject, Course, Lesson, Lecture, TutorProfile, MentorProfile, AvailabilitySlot]
    return {model.__name__: model.objects.count() for model in models}


@pytest.mark.django_db
def test_seed_demo_creates_the_expected_data():
    # Tests run with DEBUG=False, so --force is needed (see the command's safety check).
    call_command("seed_demo", "--force")

    counts = row_counts()
    assert counts["Subject"] == 5
    assert counts["Course"] == 10
    assert counts["Lesson"] == 40
    assert counts["Lecture"] == 5
    assert counts["TutorProfile"] == 5
    assert counts["MentorProfile"] == 3
    assert counts["AvailabilitySlot"] == (5 + 3) * 6


@pytest.mark.django_db
def test_seed_demo_is_safe_to_run_twice():
    call_command("seed_demo", "--force")
    first = row_counts()

    call_command("seed_demo", "--force")

    assert row_counts() == first


@pytest.mark.django_db
def test_seed_demo_refuses_without_force_when_debug_is_off():
    with pytest.raises(CommandError):
        call_command("seed_demo")

    assert Subject.objects.count() == 0


@pytest.mark.django_db
def test_seeded_data_is_visible_in_the_public_api():
    call_command("seed_demo", "--force")
    client = APIClient()

    assert len(client.get("/api/v1/courses/").json()) == 10
    assert len(client.get("/api/v1/lectures/").json()) == 5
    assert len(client.get("/api/v1/tutors/").json()) == 5
    assert len(client.get("/api/v1/mentors/").json()) == 3
