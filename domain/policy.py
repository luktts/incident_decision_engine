from dataclasses import dataclass
from typing import Callable, List


@dataclass(frozen=True)
class Policy:
    name: str
    condition: Callable
    actions: List[str]
    priority: str
