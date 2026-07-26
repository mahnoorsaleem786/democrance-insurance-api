"""Service for recording policy state changes."""

from .models import Policy, PolicyHistory


class PolicyHistoryService:
    """Service for persisting policy state transition records."""

    @staticmethod
    def log(
        policy: Policy,
        previous_state: str,
        new_state: str,
    ) -> None:
        """Create a history entry for a policy state change."""

        PolicyHistory.objects.create(
            policy=policy,
            previous_state=previous_state,
            new_state=new_state,
        )