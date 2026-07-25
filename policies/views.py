from django.db import transaction

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.models import Customer
from .models import Policy
from .serializers import QuoteSerializer
from .services import QuoteService


class CreateQuoteAPIView(CreateAPIView):
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = Customer.objects.get(
            id=serializer.validated_data["customer_id"]
        )

        quote = QuoteService.calculate_quote(customer)

        policy = Policy.objects.create(
            customer=customer,
            policy_type=serializer.validated_data["policy_type"],
            premium=quote["premium"],
            cover=quote["cover"],
            state=Policy.PolicyState.QUOTED,
        )

        return Response(
            {
                "message": "Quote generated successfully.",
                "data": {
                    "policy_id": policy.id,
                    "customer_id": customer.id,
                    "policy_type": policy.policy_type,
                    "premium": policy.premium,
                    "cover": policy.cover,
                    "state": policy.state,
                },
            },
            status=status.HTTP_201_CREATED,
        )