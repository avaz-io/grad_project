from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Level(models.TextChoices):
    """Learner levels, shared by courses, tutors and placement results.

    General subjects use Beginner/Intermediate/Advanced; English uses CEFR A1-C2.
    """

    BEGINNER = "beginner", "Beginner"
    INTERMEDIATE = "intermediate", "Intermediate"
    ADVANCED = "advanced", "Advanced"
    A1 = "a1", "A1"
    A2 = "a2", "A2"
    B1 = "b1", "B1"
    B2 = "b2", "B2"
    C1 = "c1", "C1"
    C2 = "c2", "C2"


class ContentLanguage(models.TextChoices):
    """Language a course, lecture or tutor is taught in."""

    ENGLISH = "en", "English"
    UZBEK = "uz", "Uzbek"
    RUSSIAN = "ru", "Russian"


class Subject(models.Model):
    """Shared list of subjects (Mathematics, English, ...) used across the platform."""

    slug = models.SlugField(unique=True)
    name_en = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)
    uses_cefr = models.BooleanField(default=False, help_text="Use A1-C2 levels (English).")

    class Meta:
        ordering = ["name_en"]

    def __str__(self):
        return self.name_en


class Course(models.Model):
    """A self-paced course. Hidden from students until an admin approves it."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Waiting for approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    educator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses_created",
        limit_choices_to={"role": "educator"},
    )
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="courses")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=Level.choices)
    language = models.CharField(max_length=2, choices=ContentLanguage.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="0 = free")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    rejection_reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Many-to-many: students <-> courses, stored in the Enrollment table.
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Enrollment", related_name="enrolled_courses"
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(condition=Q(price__gte=0), name="course_price_not_negative"),
        ]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """One ordered lesson inside a course: a video, a PDF or a quiz."""

    class LessonType(models.TextChoices):
        VIDEO = "video", "Video"
        PDF = "pdf", "PDF"
        QUIZ = "quiz", "Quiz"

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=10, choices=LessonType.choices)
    order = models.PositiveIntegerField(help_text="Position inside the course, starting at 1.")
    video_file = models.FileField(upload_to="lessons/videos/", blank=True)
    pdf_file = models.FileField(upload_to="lessons/pdfs/", blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    is_free_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ["course", "order"]
        constraints = [
            models.UniqueConstraint(fields=["course", "order"], name="unique_lesson_order_per_course"),
        ]

    def __str__(self):
        return f"{self.order}. {self.title}"


class Enrollment(models.Model):
    """A student's place in a course. Paid courses stay pending until payment succeeds."""

    class Status(models.TextChoices):
        PENDING_PAYMENT = "pending_payment", "Waiting for payment"
        ACTIVE = "active", "Active"
        CANCELLED = "cancelled", "Cancelled"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING_PAYMENT
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # A student can enrol in the same course only once.
            models.UniqueConstraint(fields=["student", "course"], name="unique_enrollment"),
        ]

    def __str__(self):
        return f"{self.student} in {self.course}"


class LessonProgress(models.Model):
    """Whether a student finished a lesson (and their quiz score for quiz lessons)."""

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress")
    is_completed = models.BooleanField(default=False)
    quiz_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percent, quiz lessons only.",
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "lesson progress"
        constraints = [
            models.UniqueConstraint(fields=["enrollment", "lesson"], name="unique_progress_per_lesson"),
        ]

    def __str__(self):
        return f"{self.enrollment.student} - {self.lesson}"
