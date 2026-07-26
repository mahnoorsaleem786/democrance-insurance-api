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

    def validate_dob(self, value):
        """Reject dates of birth that fall in the future."""

        if value > date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be in the future."
            )

        return value
