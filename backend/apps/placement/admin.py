from django.contrib import admin

from .models import AttemptAnswer, Choice, PlacementAttempt, PlacementTest, Question, StudentLevel


@admin.register(PlacementTest)
class PlacementTestAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "question_count", "is_active")
    list_filter = ("is_active", "subject")


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "placement_test", "lesson", "difficulty")
    list_filter = ("placement_test", "difficulty")
    search_fields = ("text",)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")


class AttemptAnswerInline(admin.TabularInline):
    model = AttemptAnswer
    extra = 0


@admin.register(PlacementAttempt)
class PlacementAttemptAdmin(admin.ModelAdmin):
    list_display = ("student", "placement_test", "status", "score", "started_at")
    list_filter = ("status", "placement_test")
    inlines = [AttemptAnswerInline]


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ("attempt", "question", "choice", "is_correct", "answered_at")


@admin.register(StudentLevel)
class StudentLevelAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "level", "score", "assessed_at")
    list_filter = ("subject", "level")
