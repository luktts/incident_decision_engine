import json
from pathlib import Path

from domain.policy import Policy


def load_policies(json_path: str):
    path = Path(json_path)

    with path.open(encoding="utf-8") as f:
        raw_policies = json.load(f)

    policies = []

    for raw in raw_policies:
        name = raw["name"]
        conditions = raw["conditions"]
        actions = raw["actions"]
        priority = raw["priority"]

        condition_fn = build_condition(conditions)

        policies.append(
            Policy(
                name=name,
                condition=condition_fn,
                actions=actions,
                priority=priority
            )
        )

    return policies

def build_condition(conditions: dict):
    def condition(incident, sla):
        for key, expected in conditions.items():

            if key == "sla_paused":
                if sla.paused != expected:
                    return False

            elif key == "sla_percentage_gte":
                if sla.percentage < expected:
                    return False

            elif key == "impact":
                if incident.impact != expected:
                    return False

            else:
                raise ValueError(f"Unknown condition: {key}")

        return True

    return condition