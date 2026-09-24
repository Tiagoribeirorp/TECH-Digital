"""Resolve equipped weapons, armor and shields for combat.

The resolver connects inventory instances to their definitions. It exposes only
values explicitly present in the equipment data; it does not invent combat
formulas.
"""

from dataclasses import dataclass
from collections.abc import Mapping

from engine.rpg.character.state import CharacterState
from engine.rpg.equipment.definitions import (
    ArmorDefinition,
    EquipmentDefinition,
    ShieldDefinition,
    WeaponDefinition,
)


@dataclass(frozen=True)
class EquippedCombatEquipment:
    weapon: WeaponDefinition | None = None
    armor: ArmorDefinition | None = None
    shield: ShieldDefinition | None = None


def resolve_equipped_combat_equipment(
    character: CharacterState,
    definitions: Mapping[str, EquipmentDefinition],
) -> EquippedCombatEquipment:
    resolved: list[EquipmentDefinition] = []

    for instance in character.inventory.items:
        if not instance.equipped:
            continue
        definition = definitions.get(instance.definition_id)
        if definition is not None:
            resolved.append(definition)

    weapon = next((item for item in resolved if isinstance(item, WeaponDefinition)), None)
    armor = next((item for item in resolved if isinstance(item, ArmorDefinition)), None)
    shield = next((item for item in resolved if isinstance(item, ShieldDefinition)), None)

    return EquippedCombatEquipment(weapon=weapon, armor=armor, shield=shield)
