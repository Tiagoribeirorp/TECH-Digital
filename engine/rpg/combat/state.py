"""Combat state for the T.E.C.H. Digital RPG Engine prototype.

This module models combat flow without inventing unresolved attack or damage formulas.
The combat engine is responsible for ordering and state transitions; concrete attack,
defense and damage values are supplied by rules that are already validated.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from engine.rpg.character.state import CharacterState


class CombatPhase(str, Enum):
    SETUP = "setup"
    DECLARATION = "declaration"
    EXECUTION = "execution"
    FINISHED = "finished"


@dataclass
class CombatantState:
    character: CharacterState
    current_hp: int
    current_fatigue: int
    available_speed: float
    initiative_result: int | None = None
    declared_action: str | None = None
    status: str = "active"

    @classmethod
    def from_character(cls, character: CharacterState) -> "CombatantState":
        character.initialize_resources()
        stats = character.derive_stats()
        return cls(
            character=character,
            current_hp=character.current_hp or stats.hp_max,
            current_fatigue=character.current_fatigue or stats.fatigue_max,
            available_speed=stats.speed_per_turn,
        )

    @property
    def is_active(self) -> bool:
        return self.status == "active" and self.current_hp > 0


@dataclass
class CombatState:
    participants: list[CombatantState]
    round_number: int = 0
    phase: CombatPhase = CombatPhase.SETUP
    initiative_order: list[str] = field(default_factory=list)
    combat_log: list[dict[str, Any]] = field(default_factory=list)
    status: str = "pending"

    def get_combatant(self, character_id: str) -> CombatantState:
        for combatant in self.participants:
            if combatant.character.id == character_id:
                return combatant
        raise KeyError(f"Unknown combatant: {character_id}")
