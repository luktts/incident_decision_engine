from domain.decision import Decision


class DecisionEngine:
    def __init__(self, policies):
        self.policies = policies

    def evaluate(self, incident, sla) -> Decision:
        for policy in self.policies:
            if policy.condition(incident, sla):
                return Decision(
                    incident_number=incident.number,
                    assignment_group=incident.assignment_group,
                    actions=policy.actions,
                    priority=policy.priority,
                    policy_applied=policy.name
                )

        return Decision(
            incident_number=incident.number,
            assignment_group=incident.assignment_group,
            actions=["No action required"],
            priority="low",
            policy_applied="default_policy"
        )
