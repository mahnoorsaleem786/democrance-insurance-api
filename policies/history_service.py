"""Service for recording policy state changes."""

from .models import PolicyHistory


class PolicyHistoryService:
    """Persists policy state transition records."""

    @staticmethod
    def log(policy, previous_state, new_state):
        """Create a history entry for a policy state change."""

        PolicyHistory.objects.create(
            policy=policy,
            previous_state=previous_state,
            new_state=new_state,
        )
