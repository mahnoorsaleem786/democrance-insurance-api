from django.db import models
from customers.models import Customer


class Policy(models.Model):

    class PolicyType(models.TextChoices):
        PERSONAL_ACCIDENT = "personal-accident", "Personal Accident"
        HEALTH = "health", "Health"
        LIFE = "life", "Life"

    class PolicyState(models.TextChoices):
        NEW = "NEW", "New"
        QUOTED = "QUOTED", "Quoted"
        ACTIVE = "ACTIVE", "Active"

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="policies",
    )

    policy_type = models.CharField(
        max_length=50,
        choices=PolicyType.choices,
    )

    premium = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    cover = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    state = models.CharField(
        max_length=20,
        choices=PolicyState.choices,
        default=PolicyState.NEW,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "policies"

    def __str__(self):
        return f"{self.customer} - {self.policy_type}"
    

class PolicyHistory(models.Model):

    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name="history",
    )

    previous_state = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    new_state = models.CharField(
        max_length=20,
    )

    changed_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "policy_history"
        ordering = ["changed_at"]

    def __str__(self):
        return f"{self.policy.id}: {self.previous_state} -> {self.new_state}"