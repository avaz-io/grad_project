from django.utils import timezone
from rest_framework import serializers

from .models import ACTIVE_BOOKING_STATUSES, AvailabilitySlot, MentorProfile, TutorProfile, TutorSubject


class TutorSubjectSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(source="subject.slug", read_only=True)
    name_en = serializers.CharField(source="subject.name_en", read_only=True)
    name_uz = serializers.CharField(source="subject.name_uz", read_only=True)

    class Meta:
        model = TutorSubject
        fields = ["slug", "name_en", "name_uz", "min_level", "max_level"]


class FreeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilitySlot
        fields = ["id", "starts_at", "ends_at", "price"]


def free_slots_of(user):
    """Future, active slots of a host that nobody has booked yet.

    A slot with only declined/cancelled bookings counts as free again.
    """
    return (
        AvailabilitySlot.objects.filter(host=user, is_active=True, starts_at__gt=timezone.now())
        .exclude(bookings__status__in=ACTIVE_BOOKING_STATUSES)
        .order_by("starts_at")
    )


# ---------- tutors ----------

class TutorListSerializer(serializers.ModelSerializer):
    # The profile's primary key is the user id, so it is also the tutor's id in the API.
    id = serializers.IntegerField(source="user_id", read_only=True)
    name = serializers.CharField(source="user.get_full_name", read_only=True)
    subjects = TutorSubjectSerializer(source="tutor_subjects", many=True, read_only=True)

    class Meta:
        model = TutorProfile
        fields = ["id", "name", "hourly_rate", "languages", "subjects", "rating_avg", "rating_count"]


class TutorDetailSerializer(TutorListSerializer):
    free_slots = serializers.SerializerMethodField()

    class Meta(TutorListSerializer.Meta):
        fields = TutorListSerializer.Meta.fields + ["bio", "free_slots"]

    def get_free_slots(self, profile):
        return FreeSlotSerializer(free_slots_of(profile.user), many=True).data


# ---------- mentors ----------

class MentorListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user_id", read_only=True)
    name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = MentorProfile
        fields = ["id", "name", "topics", "default_price", "languages", "rating_avg", "rating_count"]


class MentorDetailSerializer(MentorListSerializer):
    free_slots = serializers.SerializerMethodField()

    class Meta(MentorListSerializer.Meta):
        fields = MentorListSerializer.Meta.fields + ["bio", "free_slots"]

    def get_free_slots(self, profile):
        return FreeSlotSerializer(free_slots_of(profile.user), many=True).data
