import pytest
from django.apps import apps
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse

OUR_APPS = ["accounts", "courses", "lectures", "bookings", "placement", "payments"]


def test_every_model_is_registered_in_admin():
    for app_label in OUR_APPS:
        for model in apps.get_app_config(app_label).get_models():
            assert admin.site.is_registered(model), f"{model.__name__} is not in Django admin"


@pytest.mark.django_db
def test_admin_list_and_add_pages_open(client):
    superuser = get_user_model().objects.create_superuser(
        username="boss", email="boss@example.com", password="pass12345"
    )
    client.force_login(superuser)

    for app_label in OUR_APPS:
        for model in apps.get_app_config(app_label).get_models():
            meta = model._meta
            for page in ("changelist", "add"):
                url = reverse(f"admin:{meta.app_label}_{meta.model_name}_{page}")
                assert client.get(url).status_code == 200, url
