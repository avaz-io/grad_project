from rest_framework import serializers

from .models import Course, Lesson, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "slug", "name_en", "name_uz", "uses_cefr"]


class SubjectShortSerializer(serializers.ModelSerializer):
    """Small version of a subject, nested inside courses, lectures and tutors."""

    class Meta:
        model = Subject
        fields = ["slug", "name_en", "name_uz"]


class LessonOutlineSerializer(serializers.ModelSerializer):
    """Public course outline. File fields are left out on purpose:
    paid files are served only after an enrolment check (see CLAUDE.md)."""

    class Meta:
        model = Lesson
        fields = ["id", "order", "title", "lesson_type", "duration_minutes", "is_free_preview"]


class CourseListSerializer(serializers.ModelSerializer):
    subject = SubjectShortSerializer(read_only=True)
    educator_name = serializers.CharField(source="educator.get_full_name", read_only=True)
    # Filled in by .annotate() in the viewset, so there is no extra query per course.
    lesson_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "title", "subject", "level", "language", "price",
            "educator_name", "lesson_count", "created_at",
        ]


class CourseDetailSerializer(CourseListSerializer):
    lessons = LessonOutlineSerializer(many=True, read_only=True)

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + ["description", "lessons"]
