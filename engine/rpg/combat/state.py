"""Combat state for the T.E.C.H. Digital RPG Engine prototype."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from engine.rpg.character.effective import derive_effective_stats
from engine.rpg.character.modifiers import ModifierSource
from engine.rpg.character.state import CharacterState
from engine.rpg.core.resolution import ResolutionRecord
from engine.rpg.equipment.definitions import EquipmentDefinition
from engine.rpg.equipment.resolver import equipment_modifier_sources
from engine.rpg.combat.equipment import EquippedCombatEquipment, resolve_equipped_combat_equipment


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
    equipped_combat_equipment: EquippedCombatEquipment = field(default_factory=EquippedCombatEquipment)

    @classmethod
    def from_character(
        cls,
        character: CharacterState,
        *,
        modifier_sources: tuple[ModifierSource, ...] = (),
        equipment_definitions: dict[str, EquipmentDefinition] | None = None,
    ) -> "CombatantState":
        character.initialize_resources()
        resolved_equipment = {} if equipment_definitions is None else dict(equipment_definitions)
        equipped_combat_equipment = resolve_equipped_combat_equipment(character, resolved_equipment)
        equipped_ids = {item.definition_id for item in character.inventory.items if item.equipped}
        equipped_definitions = {key: value for key, value in resolved_equipment.items() if key in equipped_ids}
        equipment_sources = equipment_modifier_sources(equipped_definitions)
        combined_sources = tuple(modifier_sources) + equipment_sources
        stats = derive_effective_stats(character, *combined_sources)
        return cls(
            character=character,
            current_hp=character.current_hp if character.current_hp is not None else stats.hp_max,
            current_fatigue=character.current_fatigue if character.current_fatigue is not None else stats.fatigue_max,
            available_speed=stats.speed_per_turn,
            modifier_sources=combined_sources,
            equipped_combat_equipment=equipped_combat_equipment,
        )

    def effective_stats(self):
        return derive_effective_stats(self.character, *self.modifier_sources)

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
    resolution_log: list[ResolutionRecord] = field(default_factory=list)
    status: str = "pending"

    def get_combatant(self, character_id: str) -> CombatantState:
        for combatant in self.participants:
            if combatant.character.id == character_id:
                return combatant
        raise KeyError(f"Unknown combatant: {character_id}")
