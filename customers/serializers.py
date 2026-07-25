from datetime import date

from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = (
            "id",
            "first_name",
            "last_name",
            "dob",
        )

    def validate_dob(self, value):

        if value > date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be in the future."
            )

        return value