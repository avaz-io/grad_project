from django.contrib import admin

from .models import Lecture, LectureRegistration


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("title", "lecture_type", "subject", "language", "starts_at", "is_published", "zoom_status")
    list_filter = ("lecture_type", "is_published", "subject", "language", "zoom_status")
    search_fields = ("title",)


@admin.register(LectureRegistration)
class LectureRegistrationAdmin(admin.ModelAdmin):
    list_display = ("lecture", "user", "registered_at")
