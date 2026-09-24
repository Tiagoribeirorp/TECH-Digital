"""Temporary defensive choices for the current combat round."""

from dataclasses import dataclass
from enum import Enum


class DefenseChoice(str, Enum):
    NONE = "none"
    DODGE = "dodge"
    PARRY = "parry"
    BLOCK = "block"


@dataclass(frozen=True)
class DefenseChoiceState:
    choice: DefenseChoice = DefenseChoice.NONE
    weapon_speed: float | None = None
    shield_block_bonus: int = 0
