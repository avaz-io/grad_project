from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Lecture
from .serializers import LectureSerializer


class LectureViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/lectures/ and /api/v1/lectures/<id>/ (public). Published lectures only."""

    queryset = Lecture.objects.filter(is_published=True).select_related("subject", "created_by")
    serializer_class = LectureSerializer
    permission_classes = [AllowAny]
