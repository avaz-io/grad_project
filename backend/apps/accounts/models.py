from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model. The `role` decides what the user may do in the API."""

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        EDUCATOR = "educator", "Educator"
        TUTOR = "tutor", "Tutor"
        MENTOR = "mentor", "Mentor"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
