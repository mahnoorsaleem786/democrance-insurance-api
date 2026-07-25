from django.db import transaction

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.models import Customer
from .models import Policy, PolicyHistory
from .serializers import QuoteSerializer, AcceptQuoteSerializer, PolicyHistorySerializer
from .services import QuoteService
from .history_service import PolicyHistoryService


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

        PolicyHistoryService.log(
            policy=policy,
            previous_state=None,
            new_state=Policy.PolicyState.QUOTED,
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
    

class AcceptQuoteAPIView(CreateAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = AcceptQuoteSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        policy = get_object_or_404(
            Policy,
            id=serializer.validated_data["policy_id"],
        )

        if policy.state != Policy.PolicyState.QUOTED:

            return Response(
                {
                    "error": "Only quoted policies can be activated."
                },
                status=400,
            )

        previous = policy.state

        policy.state = Policy.PolicyState.ACTIVE

        policy.save()

        PolicyHistoryService.log(
            policy,
            previous,
            Policy.PolicyState.ACTIVE,
        )

        return Response(
            {
                "message": "Policy activated successfully."
            }
        )
    

class PolicyHistoryAPIView(ListAPIView):

    serializer_class = PolicyHistorySerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return PolicyHistory.objects.filter(
            policy_id=self.kwargs["pk"]
        )