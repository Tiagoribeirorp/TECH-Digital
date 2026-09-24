"""Effective character statistics derived from base state and modifiers."""

from engine.rpg.character.modifiers import EffectiveAttributes, ModifierSource, effective_attributes
from engine.rpg.character.state import CharacterState, DerivedStats


def derive_effective_stats(
    character: CharacterState,
    *sources: ModifierSource,
) -> DerivedStats:
    """Derive secondary stats from effective attributes.

    The formulas are the same confirmed formulas used by CharacterState,
    but operate on the non-mutating effective attribute view.
    """
    attributes = effective_attributes(character.attributes, *sources)

    return DerivedStats(
        reaction=attributes.as_dict()["charisma"],
        evasion=(
            attributes.as_dict()["reflexes"]
            + attributes.as_dict()["perception"]
        ) / 4,
        parry=None,
        block=None,
        senses=attributes.as_dict()["perception"],
        reaction_time_base=attributes.as_dict()["perception"],
        speed_per_turn=attributes.as_dict()["reflexes"] / 2,
        movement_per_speed=1.5,
        hp_max=attributes.as_dict()["health"],
        fatigue_max=attributes.as_dict()["willpower"],
    )


def effective_attributes_for_character(
    character: CharacterState,
    *sources: ModifierSource,
) -> EffectiveAttributes:
    return effective_attributes(character.attributes, *sources)
