from rest_framework import serializers

from customers.models import Customer
from .models import Policy


class QuoteSerializer(serializers.Serializer):

    customer_id = serializers.IntegerField()

    policy_type = serializers.ChoiceField(
        choices=Policy.PolicyType.choices
    )

    def validate_customer_id(self, value):

        if not Customer.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Customer does not exist."
            )

        return value