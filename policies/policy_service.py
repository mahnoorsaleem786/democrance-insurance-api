"""Business logic for policy creation and activation."""

from django.db import transaction
from django.shortcuts import get_object_or_404

from customers.models import Customer

from .history_service import PolicyHistoryService
from .models import Policy
from .services import QuoteService


class PolicyService:
    """Service responsible for policy business operations."""

    @staticmethod
    @transaction.atomic
    def create_quote(
        customer_id: int,
        policy_type: str,
    ) -> Policy:
        """
        Create a quoted policy for an existing customer.

        Calculates the quote, creates the policy and records
        the initial state transition.
        """

        customer = get_object_or_404(
            Customer,
            id=customer_id,
        )

        quote = QuoteService.calculate_quote(customer)

        policy = Policy.objects.create(
            customer=customer,
            policy_type=policy_type,
            premium=quote["premium"],
            cover=quote["cover"],
            state=Policy.PolicyState.QUOTED,
        )

        PolicyHistoryService.log(
            policy=policy,
            previous_state=None,
            new_state=Policy.PolicyState.QUOTED,
        )

        return policy

    @staticmethod
    @transaction.atomic
    def activate_quote(policy: Policy) -> bool:
        """
        Activate a quoted policy.

        Returns:
            True if activation succeeds.
            False if the policy is not in QUOTED state.
        """

        if policy.state != Policy.PolicyState.QUOTED:
            return False

        previous_state = policy.state

        policy.state = Policy.PolicyState.ACTIVE
        policy.save(update_fields=["state"])

        PolicyHistoryService.log(
            policy=policy,
            previous_state=previous_state,
            new_state=Policy.PolicyState.ACTIVE,
        )

        return True