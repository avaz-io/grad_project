from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.lectures.models import Lecture


def make_lecture(subject, title, is_published=True, lecture_type="recorded", **extra):
    return Lecture.objects.create(
        subject=subject, title=title, language="en", lecture_type=lecture_type,
        is_published=is_published, **extra,
    )


@pytest.mark.django_db
def test_lecture_list_shows_only_published(subject):
    make_lecture(subject, "Public")
    make_lecture(subject, "Not ready", is_published=False)

    response = APIClient().get("/api/v1/lectures/")

    assert response.status_code == 200
    assert [lecture["title"] for lecture in response.json()] == ["Public"]


@pytest.mark.django_db
def test_unpublished_lecture_detail_returns_404(subject):
    hidden = make_lecture(subject, "Not ready", is_published=False)

    response = APIClient().get(f"/api/v1/lectures/{hidden.id}/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_live_lecture_detail_hides_zoom_link(subject):
    live = make_lecture(
        subject, "Live Q&A",
        lecture_type="live",
        starts_at=timezone.now() + timedelta(days=3),
        zoom_link="https://zoom.us/j/123",
    )

    response = APIClient().get(f"/api/v1/lectures/{live.id}/")

    assert response.status_code == 200
    assert response.json()["lecture_type"] == "live"
    # Only registered users may see the link, so the public API never sends it.
    assert "zoom_link" not in response.json()
    assert "zoom.us" not in response.content.decode()
