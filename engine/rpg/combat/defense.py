"""Defense selection and value resolution for combat.

The source confirms several defensive concepts and some of their modifiers,
but does not yet define a universal attack-versus-defense formula. This module
therefore exposes defense values without deciding that final comparison.
"""

from dataclasses import dataclass
from enum import Enum

from engine.rpg.character.state import CharacterState
from engine.rpg.character.effective import derive_effective_stats
from engine.rpg.combat.equipment import EquippedCombatEquipment
from engine.rpg.combat.defense_equipment import EquipmentDefenseContext, defense_equipment_context


class DefenseMode(str, Enum):
    EVASION = "evasion"
    PARRY = "parry"
    BLOCK = "block"
    DODGE = "dodge"


@dataclass(frozen=True)
class DefenseResolution:
    mode: DefenseMode
    value: float
    modifier: int = 0


def resolve_defense(
    character: CharacterState,
    mode: DefenseMode,
    *,
    parry_skill: int | None = None,
    shield_skill: int | None = None,
    modifier: int = 0,
    equipment: EquippedCombatEquipment | None = None,
) -> DefenseResolution:
    """Return the selected defense value from confirmed derived statistics."""
    stats = derive_effective_stats(character)
    equipment_context: EquipmentDefenseContext | None = None
    if equipment is not None:
        equipment_context = defense_equipment_context(equipment)

    if mode is DefenseMode.EVASION:
        value = stats.evasion
    elif mode is DefenseMode.PARRY:
        if parry_skill is None:
            raise ValueError("Parry requires the relevant skill value")
        value = parry_skill / 2
    elif mode is DefenseMode.BLOCK:
        if shield_skill is None:
            raise ValueError("Block requires the shield skill value")
        value = shield_skill / 2
        if equipment_context is not None:
            value += equipment_context.shield_block_bonus
    elif mode is DefenseMode.DODGE:
        value = stats.evasion
    else:
        raise ValueError(f"Unsupported defense mode: {mode}")

    return DefenseResolution(mode=mode, value=value, modifier=modifier)
