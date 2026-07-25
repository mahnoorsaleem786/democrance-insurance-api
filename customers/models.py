from django.db import models
from django.core.validators import MinLengthValidator


class Customer(models.Model):
    first_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )

    last_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )

    dob = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "customers"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"