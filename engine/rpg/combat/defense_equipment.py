"""Combat equipment-aware defense context.

The source defines armor as Defense + Durability and shields as enabling Block,
with a large shield granting +1 to the test. This module keeps those values
separate from the still-unresolved universal attack-vs-defense formula.
"""

from dataclasses import dataclass

from engine.rpg.combat.equipment import EquippedCombatEquipment


@dataclass(frozen=True)
class EquipmentDefenseContext:
    armor_defense: int | None
    armor_durability: int | None
    shield_block_bonus: int
    shield_durability: int | None


def defense_equipment_context(
    equipment: EquippedCombatEquipment,
) -> EquipmentDefenseContext:
    armor = equipment.armor
    shield = equipment.shield
    return EquipmentDefenseContext(
        armor_defense=None if armor is None else armor.defense_bonus,
        armor_durability=None if armor is None else armor.durability,
        shield_block_bonus=0 if shield is None else shield.block_bonus,
        shield_durability=None if shield is None else shield.durability,
    )
