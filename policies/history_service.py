from .models import PolicyHistory


class PolicyHistoryService:

    @staticmethod
    def log(policy, previous_state, new_state):

        PolicyHistory.objects.create(
            policy=policy,
            previous_state=previous_state,
            new_state=new_state,
        )