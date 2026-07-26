"""Serializers for customer API endpoints."""

from datetime import date

from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for creating and listing customers."""

    class Meta:
        model = Customer
        fields = (
            "id",
            "first_name",
            "last_name",
            "dob",
        )

    @staticmethod
    def _validate_name(value: str, field_name: str) -> str:
        """Validate a customer's name field."""

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                f"{field_name} cannot be empty."
            )

        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                f"{field_name} should contain only alphabetic characters."
            )

        return value

    def validate_first_name(self, value: str) -> str:
        """Validate the customer's first name."""
        return self._validate_name(value, "First name")

    def validate_last_name(self, value: str) -> str:
        """Validate the customer's last name."""
        return self._validate_name(value, "Last name")

    def validate_dob(self, value: date) -> date:
        """Reject dates of birth that fall in the future."""

        if value > date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be in the future."
            )

        return value