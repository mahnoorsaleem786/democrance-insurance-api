from rest_framework import serializers

from customers.models import Customer
from .models import Policy, PolicyHistory


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
    

class AcceptQuoteSerializer(serializers.Serializer):

    policy_id = serializers.IntegerField()


class PolicyHistorySerializer(serializers.ModelSerializer):

    class Meta:

        model = PolicyHistory

        fields = "__all__"