from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "currency", "provider", "status", "created_at", "paid_at")
    list_filter = ("status", "provider")
    search_fields = ("user__username", "user__email", "provider_payment_id")
