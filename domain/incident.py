from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Incident:
    number: str
    short_description: str
    assignment_group: str
    impact: int
    urgency: int
    opened_at: datetime