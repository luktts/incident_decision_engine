from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Decision:
    incident_number: str
    assignment_group: str
    actions: List[str]
    priority: str
    policy_applied: str