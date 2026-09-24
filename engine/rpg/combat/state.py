"""Combat state for the T.E.C.H. Digital RPG Engine prototype."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from engine.rpg.character.effective import derive_effective_stats
from engine.rpg.character.modifiers import ModifierSource
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
    modifier_sources: tuple[ModifierSource, ...] = ()

    @classmethod
    def from_character(
        cls,
        character: CharacterState,
        *,
        modifier_sources: tuple[ModifierSource, ...] = (),
    ) -> "CombatantState":
        character.initialize_resources()
        stats = derive_effective_stats(character, *modifier_sources)
        return cls(
            character=character,
            current_hp=character.current_hp or stats.hp_max,
            current_fatigue=character.current_fatigue or stats.fatigue_max,
            available_speed=stats.speed_per_turn,
            modifier_sources=modifier_sources,
        )

    def effective_stats(self):
        return derive_effective_stats(
            self.character,
            *self.modifier_sources,
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
