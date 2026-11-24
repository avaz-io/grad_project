from django.contrib import admin

from .models import Course, Enrollment, Lesson, LessonProgress, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_uz", "slug", "uses_cefr")
    prepopulated_fields = {"slug": ("name_en",)}


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "educator", "subject", "level", "language", "price", "status")
    list_filter = ("status", "subject", "level", "language")
    search_fields = ("title", "educator__username")
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "lesson_type", "order", "is_free_preview")
    list_filter = ("lesson_type",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "status", "enrolled_at")
    list_filter = ("status",)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "lesson", "is_completed", "quiz_score", "completed_at")
    list_filter = ("is_completed",)
