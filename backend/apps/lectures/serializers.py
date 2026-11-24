from rest_framework import serializers

from apps.courses.serializers import SubjectShortSerializer

from .models import Lecture


class LectureSerializer(serializers.ModelSerializer):
    """Public lecture data. The Zoom link is left out on purpose:
    only users registered for a live lecture may see it (see docs/er-diagram.md)."""

    subject = SubjectShortSerializer(read_only=True)
    speaker_name = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = [
            "id", "title", "description", "subject", "language", "lecture_type",
            "video_file", "starts_at", "duration_minutes", "speaker_name", "created_at",
        ]

    def get_speaker_name(self, lecture):
        # created_by can be empty if the user account was deleted.
        return lecture.created_by.get_full_name() if lecture.created_by else ""
