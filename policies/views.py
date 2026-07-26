"""API views for policy quotes, activation, and listing."""

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Policy, PolicyHistory
from .policy_service import PolicyService
from .serializers import (
    AcceptQuoteSerializer,
    PolicyHistorySerializer,
    PolicySerializer,
    QuoteSerializer,
)

from common.logger import logger


class CreateQuoteAPIView(CreateAPIView):
    """Generate a quoted policy for an existing customer."""

    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]

    def create(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """Generate a quote and create a policy."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        policy = PolicyService.create_quote(
            customer_id=serializer.validated_data["customer_id"],
            policy_type=serializer.validated_data["policy_type"],
        )

        logger.info(
            "Quote generated successfully for policy %s.",
            policy.id,
        )

        return Response(
            {
                "message": "Quote generated successfully.",
                "data": {
                    "policy_id": policy.id,
                    "customer_id": policy.customer.id,
                    "policy_type": policy.policy_type,
                    "premium": policy.premium,
                    "cover": policy.cover,
                    "state": policy.state,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class AcceptQuoteAPIView(CreateAPIView):
    """Activate a quoted insurance policy."""

    serializer_class = AcceptQuoteSerializer
    permission_classes = [IsAuthenticated]

    def post(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """Activate an existing quoted policy."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        policy = get_object_or_404(
            Policy,
            id=serializer.validated_data["policy_id"],
        )

        if not PolicyService.activate_quote(policy):
            return Response(
                {
                    "error": "Only quoted policies can be activated.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(
            "Policy %s activated successfully.",
            policy.id,
        )

        return Response(
            {
                "message": "Policy activated successfully.",
            },
            status=status.HTTP_200_OK,
        )


class PolicyHistoryAPIView(ListAPIView):
    """List policy state transition history."""

    serializer_class = PolicyHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[PolicyHistory]:
        """Return the history for the requested policy."""

        return PolicyHistory.objects.filter(
            policy_id=self.kwargs["pk"],
        )


class PolicyListAPIView(ListAPIView):
    """List policies with optional filtering."""

    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Policy]:
        """Return policies filtered by the optional type parameter."""

        queryset = Policy.objects.select_related("customer")

        policy_type = self.request.query_params.get("type")

        if policy_type:
            queryset = queryset.filter(
                policy_type=policy_type,
            )

        return queryset