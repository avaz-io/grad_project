from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import MentorProfile, TutorProfile, VerificationStatus
from .serializers import (
    MentorDetailSerializer,
    MentorListSerializer,
    TutorDetailSerializer,
    TutorListSerializer,
)


class TutorViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/tutors/ and /api/v1/tutors/<id>/ (public). Verified tutors only.

    List filters (optional): ?subject=<slug>  ?language=<en|uz|ru>
    Ordered by rating for now; the weighted matching score comes in Iteration 3.
    """

    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TutorDetailSerializer
        return TutorListSerializer

    def get_queryset(self):
        queryset = (
            TutorProfile.objects.filter(verification_status=VerificationStatus.VERIFIED)
            .select_related("user")
            .prefetch_related("tutor_subjects__subject")
            .order_by("-rating_avg", "user_id")
        )
        if self.action == "retrieve":
            return queryset

        params = self.request.query_params
        if params.get("subject"):
            # No duplicates: a tutor can list each subject only once (unique constraint).
            queryset = queryset.filter(tutor_subjects__subject__slug=params["subject"])
        if params.get("language"):
            # languages is a PostgreSQL array; __contains means "the array includes this code".
            queryset = queryset.filter(languages__contains=[params["language"]])
        return queryset


class MentorViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/mentors/ and /api/v1/mentors/<id>/ (public). Verified mentors only.

    List filters (optional): ?language=<en|uz|ru>  ?topic=<text>
    Mentors have no Subject link in the database (they give career/study advice),
    so they are filtered by a word in their topics instead.
    """

    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MentorDetailSerializer
        return MentorListSerializer

    def get_queryset(self):
        queryset = (
            MentorProfile.objects.filter(verification_status=VerificationStatus.VERIFIED)
            .select_related("user")
            .order_by("-rating_avg", "user_id")
        )
        if self.action == "retrieve":
            return queryset

        params = self.request.query_params
        if params.get("language"):
            queryset = queryset.filter(languages__contains=[params["language"]])
        if params.get("topic"):
            queryset = queryset.filter(topics__icontains=params["topic"])
        return queryset
