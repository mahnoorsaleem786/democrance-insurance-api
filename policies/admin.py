from django.contrib import admin
from .models import Policy, PolicyHistory


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


@admin.register(PolicyHistory)
class PolicyHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "policy",
        "previous_state",
        "new_state",
        "changed_at",
    )