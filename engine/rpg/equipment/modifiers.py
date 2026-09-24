"""Confirmed equipment-derived attribute modifiers."""

from engine.rpg.character.modifiers import ModifierSource
from engine.rpg.equipment.definitions import ExoskeletonDefinition


def attribute_modifier_source(
    equipment: ExoskeletonDefinition,
) -> ModifierSource:
    """Expose only the confirmed exoskeleton attribute bonuses."""
    return ModifierSource(
        source_id=equipment.id,
        attribute_modifiers={
            "strength": equipment.strength_bonus,
            "reflexes": equipment.reflexes_bonus,
        },
    )
