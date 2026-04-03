from dataclasses import dataclass


@dataclass(frozen=True)
class SLA:
    name: str
    percentage: int
    paused: bool