"""Effective-stat modifiers for T.E.C.H. Digital.

Base attributes are never mutated by this layer. It calculates an effective
view from independent modifier sources such as race, equipment, and future
talents/effects.
"""

from dataclasses import dataclass, field
from typing import Mapping

from engine.rpg.character.state import Attribute, Attributes


@dataclass(frozen=True)
class ModifierSource:
    source_id: str
    attribute_modifiers: Mapping[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class EffectiveAttributes:
    base: Attributes
    modifiers: dict[str, int]

    def get(self, attribute: Attribute) -> int:
        key = attribute.value
        return self.base.get(attribute) + self.modifiers.get(key, 0)

    def as_dict(self) -> dict[str, int]:
        return {
            attribute.value: self.get(attribute)
            for attribute in Attribute
        }


def combine_attribute_modifiers(
    *sources: ModifierSource,
) -> dict[str, int]:
    """Combine modifiers without changing any source or base attribute."""
    combined: dict[str, int] = {}
    for source in sources:
        for attribute, value in source.attribute_modifiers.items():
            combined[attribute] = combined.get(attribute, 0) + value
    return combined


def effective_attributes(
    base: Attributes,
    *sources: ModifierSource,
) -> EffectiveAttributes:
    return EffectiveAttributes(
        base=base,
        modifiers=combine_attribute_modifiers(*sources),
    )
