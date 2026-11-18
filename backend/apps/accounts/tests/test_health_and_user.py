import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_health_endpoint_is_public():
    response = APIClient().get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_new_user_is_student_by_default():
    user = get_user_model().objects.create_user(username="ali", password="pass12345")
    assert user.role == "student"


@pytest.mark.django_db
def test_user_role_can_be_set():
    user = get_user_model().objects.create_user(
        username="dilnoza", password="pass12345", role="tutor"
    )
    assert user.role == "tutor"
