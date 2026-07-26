"""Admin configuration for customer models."""

from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin interface for the Customer model."""

    list_display = (
        "id",
        "first_name",
        "last_name",
        "dob",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
    )

    ordering = ("-created_at",)
