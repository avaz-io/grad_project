from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from apps.courses.models import Lesson, Level, Subject


class PlacementTest(models.Model):
    """The adaptive placement test for one subject."""

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="placement_tests")
    title = models.CharField(max_length=200)
    question_count = models.PositiveSmallIntegerField(default=10, help_text="Questions per attempt.")
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            # Only one active test per subject, so the app knows which one to use.
            models.UniqueConstraint(
                fields=["subject"], condition=Q(is_active=True), name="one_active_test_per_subject"
            ),
        ]

    def __str__(self):
        return self.title


class Question(models.Model):
    """A multiple-choice question. Belongs to a placement test OR to a quiz lesson."""

    placement_test = models.ForeignKey(
        PlacementTest, on_delete=models.CASCADE, null=True, blank=True, related_name="questions"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name="questions"
    )
    text = models.TextField()
    difficulty = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 = easiest, 5 = hardest.",
    )
    order = models.PositiveSmallIntegerField(default=0, help_text="Quiz lessons only.")

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            # Exactly one owner: a placement test or a quiz lesson, never both, never neither.
            models.CheckConstraint(
                condition=(
                    Q(placement_test__isnull=False, lesson__isnull=True)
                    | Q(placement_test__isnull=True, lesson__isnull=False)
                ),
                name="question_has_exactly_one_owner",
            ),
            models.CheckConstraint(
                condition=Q(difficulty__gte=1, difficulty__lte=5),
                name="question_difficulty_1_to_5",
            ),
        ]

    def __str__(self):
        return self.text[:60]


class Choice(models.Model):
    """One answer option. `is_correct` must never be sent to the student's browser."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class PlacementAttempt(models.Model):
    """One run of a placement test. Remembers the current difficulty between questions."""

    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In progress"
        FINISHED = "finished", "Finished"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="placement_attempts"
    )
    placement_test = models.ForeignKey(
        PlacementTest, on_delete=models.CASCADE, related_name="attempts"
    )
    current_difficulty = models.PositiveSmallIntegerField(default=3)
    score = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.placement_test} ({self.status})"


class AttemptAnswer(models.Model):
    """One answer given during an attempt."""

    attempt = models.ForeignKey(PlacementAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="attempt_answers")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="attempt_answers")
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # The same question is never asked twice in one attempt.
            models.UniqueConstraint(fields=["attempt", "question"], name="unique_answer_per_question"),
        ]

    def __str__(self):
        return f"{self.attempt} - Q{self.question_id}"


class StudentLevel(models.Model):
    """A student's current level in one subject (result of the latest finished attempt)."""

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="levels"
    )
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="student_levels")
    level = models.CharField(max_length=20, choices=Level.choices)
    score = models.PositiveSmallIntegerField(default=0)
    assessed_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student", "subject"], name="one_level_per_subject"),
        ]

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.get_level_display()}"
