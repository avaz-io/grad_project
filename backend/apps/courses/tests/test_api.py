import pytest
from rest_framework.test import APIClient

from apps.courses.models import Course, Lesson, Subject


@pytest.fixture
def client():
    # No login: these endpoints must work for anonymous visitors.
    return APIClient()


@pytest.fixture
def english():
    return Subject.objects.create(slug="english", name_en="English", name_uz="Ingliz tili", uses_cefr=True)


def make_course(educator, subject, title, status="approved", level="beginner", language="en", price="0"):
    return Course.objects.create(
        educator=educator, subject=subject, title=title,
        status=status, level=level, language=language, price=price,
    )


def titles(response):
    return {item["title"] for item in response.json()}


# ---------- subjects ----------

@pytest.mark.django_db
def test_subject_list_is_public(client, subject, english):
    response = client.get("/api/v1/subjects/")

    assert response.status_code == 200
    assert {s["slug"] for s in response.json()} == {"math", "english"}


@pytest.mark.django_db
def test_subject_detail_uses_slug(client, english):
    response = client.get("/api/v1/subjects/english/")

    assert response.status_code == 200
    assert response.json()["uses_cefr"] is True


# ---------- courses: only published ----------

@pytest.mark.django_db
def test_course_list_shows_only_approved_courses(client, educator, subject):
    make_course(educator, subject, "Published")
    for status in ["draft", "pending", "rejected"]:
        make_course(educator, subject, f"Hidden {status}", status=status)

    response = client.get("/api/v1/courses/")

    assert response.status_code == 200
    assert titles(response) == {"Published"}


@pytest.mark.django_db
def test_unpublished_course_detail_returns_404(client, educator, subject):
    draft = make_course(educator, subject, "Draft", status="draft")

    response = client.get(f"/api/v1/courses/{draft.id}/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_course_detail_lists_lessons_without_files(client, educator, subject):
    course = make_course(educator, subject, "Algebra")
    Lesson.objects.create(course=course, title="Second", lesson_type="pdf", order=2)
    Lesson.objects.create(course=course, title="First", lesson_type="video", order=1, is_free_preview=True)

    response = client.get(f"/api/v1/courses/{course.id}/")

    assert response.status_code == 200
    data = response.json()
    assert data["lesson_count"] == 2
    assert [lesson["title"] for lesson in data["lessons"]] == ["First", "Second"]
    # Paid files must never leak through the public outline.
    assert "video_file" not in data["lessons"][0]
    assert "pdf_file" not in data["lessons"][0]


@pytest.mark.django_db
def test_course_list_does_not_allow_writing(client, subject):
    response = client.post("/api/v1/courses/", {"title": "Hack"})

    assert response.status_code in (401, 403, 405)
    assert not Course.objects.filter(title="Hack").exists()


# ---------- courses: filters ----------

@pytest.fixture
def catalogue(educator, subject, english):
    make_course(educator, subject, "Algebra", level="beginner", language="uz", price="0")
    make_course(educator, subject, "Calculus", level="advanced", language="en", price="30")
    make_course(educator, english, "IELTS", level="b2", language="en", price="20")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "query, expected",
    [
        ("subject=math", {"Algebra", "Calculus"}),
        ("subject=english", {"IELTS"}),
        ("level=b2", {"IELTS"}),
        ("language=en", {"Calculus", "IELTS"}),
        ("min_price=20", {"Calculus", "IELTS"}),
        ("max_price=0", {"Algebra"}),
        ("min_price=10&max_price=25", {"IELTS"}),
        ("subject=math&language=en", {"Calculus"}),
        ("subject=unknown", set()),
    ],
)
def test_course_filters(client, catalogue, query, expected):
    response = client.get(f"/api/v1/courses/?{query}")

    assert response.status_code == 200
    assert titles(response) == expected


@pytest.mark.django_db
@pytest.mark.parametrize("query", ["min_price=abc", "max_price=-5", "min_price=NaN"])
def test_bad_price_filter_returns_400(client, query):
    response = client.get(f"/api/v1/courses/?{query}")

    assert response.status_code == 400
