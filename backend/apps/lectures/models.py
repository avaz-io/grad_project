from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.courses.models import ContentLanguage, Subject
from apps.integrations.choices import ZoomStatus


class Lecture(models.Model):
    """A free open lecture: either a recorded video or a scheduled live Zoom session."""

    class LectureType(models.TextChoices):
        RECORDED = "recorded", "Recorded"
        LIVE = "live", "Live"

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="lectures_created",
    )
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="lectures")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=2, choices=ContentLanguage.choices)
    lecture_type = models.CharField(max_length=10, choices=LectureType.choices)
    video_file = models.FileField(upload_to="lectures/", blank=True, help_text="Recorded only.")
    starts_at = models.DateTimeField(null=True, blank=True, help_text="Live only.")
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    zoom_meeting_id = models.CharField(max_length=50, blank=True)
    zoom_link = models.URLField(max_length=500, blank=True)
    zoom_status = models.CharField(
        max_length=10, choices=ZoomStatus.choices, default=ZoomStatus.NONE
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Many-to-many: users <-> live lectures, stored in the LectureRegistration table.
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="LectureRegistration", related_name="registered_lectures"
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # A live lecture must have a start time.
            models.CheckConstraint(
                condition=~Q(lecture_type="live") | Q(starts_at__isnull=False),
                name="live_lecture_has_start_time",
            ),
        ]

    def __str__(self):
        return self.title


class LectureRegistration(models.Model):
    """A user's registration for a live lecture. Only registered users see the Zoom link."""

    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lecture_registrations"
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["lecture", "user"], name="unique_lecture_registration"),
        ]

    def __str__(self):
        return f"{self.user} -> {self.lecture}"
