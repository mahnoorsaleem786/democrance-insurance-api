"""API views for policy quotes, activation, and listing."""

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.models import Customer

from .history_service import PolicyHistoryService
from .models import Policy, PolicyHistory
from .serializers import (AcceptQuoteSerializer, PolicyHistorySerializer,
                          PolicySerializer, QuoteSerializer)
from .services import QuoteService


class CreateQuoteAPIView(CreateAPIView):
    """Generate a quoted policy for an existing customer."""

    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Calculate a quote, create the policy, and log the initial state."""

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
    """Activate a policy that is currently in the QUOTED state."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Transition a quoted policy to ACTIVE and record the change."""

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
    """List state transition history for a single policy."""

    serializer_class = PolicyHistorySerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return history entries for the policy identified in the URL."""

        return PolicyHistory.objects.filter(
            policy_id=self.kwargs["pk"]
        )


class PolicyListAPIView(ListAPIView):
    """List policies with optional filtering by policy type."""

    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return policies, optionally filtered by the type query parameter."""

        queryset = Policy.objects.select_related("customer")

        policy_type = self.request.query_params.get("type")

        if policy_type:
            queryset = queryset.filter(policy_type=policy_type)

        return queryset
