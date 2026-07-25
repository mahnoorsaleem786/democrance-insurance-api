from django.contrib import admin
from .models import Policy


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "policy_type",
        "premium",
        "cover",
        "state",
    )

    search_fields = (
        "customer__first_name",
        "customer__last_name",
        "policy_type",
    )

    list_filter = (
        "state",
        "policy_type",
    )