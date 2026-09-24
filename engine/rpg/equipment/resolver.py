"""Resolve confirmed attribute effects from currently equipped definitions.

This resolver only applies effects whose values are explicitly represented
by the equipment definitions. It does not invent weapon or armor formulas.
"""

from collections.abc import Mapping

from engine.rpg.character.modifiers import ModifierSource
from engine.rpg.equipment.definitions import EquipmentDefinition, ExoskeletonDefinition
from engine.rpg.equipment.modifiers import attribute_modifier_source


def equipment_modifier_sources(
    equipped_definitions: Mapping[str, EquipmentDefinition],
) -> tuple[ModifierSource, ...]:
    sources: list[ModifierSource] = []

    for equipment in equipped_definitions.values():
        if isinstance(equipment, ExoskeletonDefinition):
            sources.append(attribute_modifier_source(equipment))

    return tuple(sources)
