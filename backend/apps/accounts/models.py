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

    class InterfaceLanguage(models.TextChoices):
        ENGLISH = "en", "English"
        UZBEK = "uz", "Uzbek"

    # Unique because users will log in with their e-mail address.
    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    preferred_language = models.CharField(
        max_length=2, choices=InterfaceLanguage.choices, default=InterfaceLanguage.ENGLISH
    )


class EducatorProfile(models.Model):
    """Public information about an educator. One profile per educator user."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="educator_profile"
    )
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Educator profile of {self.user}"
