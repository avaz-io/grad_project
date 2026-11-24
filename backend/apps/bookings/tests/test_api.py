from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from apps.bookings.models import AvailabilitySlot, Booking, MentorProfile, TutorProfile, TutorSubject
from apps.courses.models import Subject


def make_host(username, role):
    return get_user_model().objects.create_user(
        username=username, email=f"{username}@example.com", password="pass12345", role=role
    )


def make_tutor(username, status="verified", languages=("en",), subjects=()):
    profile = TutorProfile.objects.create(
        user=make_host(username, "tutor"), verification_status=status, languages=list(languages)
    )
    for subject in subjects:
        TutorSubject.objects.create(tutor=profile, subject=subject, min_level="beginner", max_level="advanced")
    return profile


def make_mentor(username, status="verified", languages=("en",), topics=""):
    return MentorProfile.objects.create(
        user=make_host(username, "mentor"), verification_status=status,
        languages=list(languages), topics=topics,
    )


def ids(response):
    return {item["id"] for item in response.json()}


@pytest.fixture
def english():
    return Subject.objects.create(slug="english", name_en="English", name_uz="Ingliz tili")


# ---------- tutors ----------

@pytest.mark.django_db
def test_tutor_list_shows_only_verified():
    verified = make_tutor("t_ok")
    make_tutor("t_pending", status="pending")
    make_tutor("t_rejected", status="rejected")

    response = APIClient().get("/api/v1/tutors/")

    assert response.status_code == 200
    assert ids(response) == {verified.user_id}


@pytest.mark.django_db
def test_unverified_tutor_detail_returns_404():
    pending = make_tutor("t_pending", status="pending")

    response = APIClient().get(f"/api/v1/tutors/{pending.user_id}/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_tutor_list_filters_by_subject(subject, english):
    math_tutor = make_tutor("t_math", subjects=[subject])
    english_tutor = make_tutor("t_eng", subjects=[english])
    both = make_tutor("t_both", subjects=[subject, english])

    response = APIClient().get("/api/v1/tutors/?subject=english")

    assert ids(response) == {english_tutor.user_id, both.user_id}
    assert math_tutor.user_id not in ids(response)


@pytest.mark.django_db
def test_tutor_list_filters_by_language():
    uzbek = make_tutor("t_uz", languages=["uz", "ru"])
    make_tutor("t_en", languages=["en"])

    response = APIClient().get("/api/v1/tutors/?language=uz")

    assert ids(response) == {uzbek.user_id}


@pytest.mark.django_db
def test_tutor_filters_combine(subject, english):
    match = make_tutor("t_match", languages=["uz"], subjects=[english])
    make_tutor("t_wrong_lang", languages=["en"], subjects=[english])
    make_tutor("t_wrong_subject", languages=["uz"], subjects=[subject])

    response = APIClient().get("/api/v1/tutors/?subject=english&language=uz")

    assert ids(response) == {match.user_id}


@pytest.mark.django_db
def test_tutor_detail_shows_only_free_future_slots(student):
    tutor = make_tutor("t_slots")
    now = timezone.now()

    def slot(hours_from_now, **extra):
        start = now + timedelta(hours=hours_from_now)
        return AvailabilitySlot.objects.create(
            host=tutor.user, starts_at=start, ends_at=start + timedelta(hours=1), **extra
        )

    free = slot(24)
    slot(-24)  # in the past
    slot(48, is_active=False)  # withdrawn by the tutor
    booked = slot(72)
    Booking.objects.create(slot=booked, student=student, booking_type="tutor_lesson", status="confirmed")
    freed = slot(96)  # its only booking was cancelled, so it is free again
    Booking.objects.create(slot=freed, student=student, booking_type="tutor_lesson", status="cancelled")

    response = APIClient().get(f"/api/v1/tutors/{tutor.user_id}/")

    assert response.status_code == 200
    assert [s["id"] for s in response.json()["free_slots"]] == [free.id, freed.id]


@pytest.mark.django_db
def test_tutor_response_does_not_expose_email():
    tutor = make_tutor("t_private")

    response = APIClient().get(f"/api/v1/tutors/{tutor.user_id}/")

    assert "@example.com" not in response.content.decode()


# ---------- mentors ----------

@pytest.mark.django_db
def test_mentor_list_shows_only_verified():
    verified = make_mentor("m_ok")
    make_mentor("m_pending", status="pending")

    response = APIClient().get("/api/v1/mentors/")

    assert response.status_code == 200
    assert ids(response) == {verified.user_id}


@pytest.mark.django_db
def test_unverified_mentor_detail_returns_404():
    pending = make_mentor("m_pending", status="pending")

    response = APIClient().get(f"/api/v1/mentors/{pending.user_id}/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_mentor_list_filters_by_language():
    russian = make_mentor("m_ru", languages=["uz", "ru"])
    make_mentor("m_en", languages=["en"])

    response = APIClient().get("/api/v1/mentors/?language=ru")

    assert ids(response) == {russian.user_id}


@pytest.mark.django_db
def test_mentor_list_filters_by_topic():
    career = make_mentor("m_career", topics="Career in IT, CV review")
    make_mentor("m_study", topics="study planning")

    response = APIClient().get("/api/v1/mentors/?topic=career")

    assert ids(response) == {career.user_id}
