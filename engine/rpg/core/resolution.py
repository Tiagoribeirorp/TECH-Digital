"""Structured mechanical resolution records."""

from dataclasses import dataclass, field
from typing import Any
import uuid


@dataclass(frozen=True)
class ResolutionRecord:
    source: str
    action: str
    actor_id: str | None = None
    target_id: str | None = None
    random_roll: int | None = None
    modifiers: dict[str, int] = field(default_factory=dict)
    effective_value: int | float | None = None
    result: str = ""
    consequences: dict[str, Any] = field(default_factory=dict)
    sequence: int = 0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
