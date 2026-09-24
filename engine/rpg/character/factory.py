"""Character construction helpers for the prototype."""

from dataclasses import replace

from .definitions import RaceDefinition
from .state import Attributes, CharacterState


def apply_race(
    character: CharacterState,
    race: RaceDefinition,
) -> CharacterState:
    values = character.attributes.as_dict()
    for attribute, modifier in race.attribute_modifiers.items():
        if attribute not in values:
            raise KeyError(f"Unknown attribute: {attribute}")
        values[attribute] += modifier

    return replace(
        character,
        race_id=race.id,
        attributes=Attributes(**values),
    )
