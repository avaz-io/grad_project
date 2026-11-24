from django.contrib import admin

from .models import AvailabilitySlot, Booking, MentorProfile, Review, TutorProfile, TutorSubject


class TutorSubjectInline(admin.TabularInline):
    model = TutorSubject
    extra = 0


@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "hourly_rate", "verification_status", "rating_avg", "rating_count")
    list_filter = ("verification_status",)
    search_fields = ("user__username", "user__email")
    inlines = [TutorSubjectInline]


@admin.register(TutorSubject)
class TutorSubjectAdmin(admin.ModelAdmin):
    list_display = ("tutor", "subject", "min_level", "max_level")
    list_filter = ("subject",)


@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "topics", "default_price", "verification_status", "rating_avg")
    list_filter = ("verification_status",)
    search_fields = ("user__username", "user__email", "topics")


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("host", "starts_at", "ends_at", "price", "is_active")
    list_filter = ("is_active",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("student", "slot", "booking_type", "status", "price", "zoom_status", "created_at")
    list_filter = ("status", "booking_type", "zoom_status")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("booking", "rating", "created_at")
    list_filter = ("rating",)
