from decimal import Decimal, InvalidOperation

from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from .models import Course, Subject
from .serializers import CourseDetailSerializer, CourseListSerializer, SubjectSerializer


def parse_price(request, name):
    """Read a price filter like ?min_price=10 from the URL. Returns None if it is not given."""
    raw = request.query_params.get(name)
    if raw in (None, ""):
        return None
    try:
        value = Decimal(raw)
    except InvalidOperation:
        raise ValidationError({name: "Must be a number."})
    if not value.is_finite() or value < 0:
        raise ValidationError({name: "Must be a number that is 0 or more."})
    return value


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/subjects/ and /api/v1/subjects/<slug>/ (public)."""

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/courses/ and /api/v1/courses/<id>/ (public).

    Only approved (published) courses are shown. List filters (all optional):
    ?subject=<slug>  ?level=<level>  ?language=<en|uz|ru>  ?min_price=<n>  ?max_price=<n>
    """

    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseListSerializer

    def get_queryset(self):
        queryset = (
            Course.objects.filter(status=Course.Status.APPROVED)
            .select_related("subject", "educator")
            .annotate(lesson_count=Count("lessons"))
        )
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("lessons")
            return queryset  # filters only apply to the list

        params = self.request.query_params
        if params.get("subject"):
            queryset = queryset.filter(subject__slug=params["subject"])
        if params.get("level"):
            queryset = queryset.filter(level=params["level"])
        if params.get("language"):
            queryset = queryset.filter(language=params["language"])

        min_price = parse_price(self.request, "min_price")
        max_price = parse_price(self.request, "max_price")
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        return queryset
