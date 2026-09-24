"""Data-driven race and capability foundations."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


@dataclass(frozen=True)
class RaceDefinition:
    id: str
    name: str
    attribute_modifiers: Mapping[str, int] = field(default_factory=dict)
    skill_modifiers: Mapping[str, int] = field(default_factory=dict)
    advantages: tuple[str, ...] = ()
    disadvantages: tuple[str, ...] = ()
    movement_rules: Mapping[str, object] = field(default_factory=dict)
    special_rules: tuple[str, ...] = ()


@dataclass(frozen=True)
class SkillDefinition:
    id: str
    name: str
    group: str
    base_attributes: tuple[str, ...]
    requires_training: bool = False
    specializations: tuple[str, ...] = ()


@dataclass
class SkillState:
    definition_id: str
    points: int = 0

    def value(self, attributes: Mapping[str, int]) -> int:
        if self.points <= 0:
            # The source defines two untrained penalties (-3/-4) depending
            # on the specific rule. This prototype does not guess which.
            raise ValueError(
                "Untrained capability value requires a source-specific penalty."
            )
        if self.points == 1:
            bonus = -2
        elif self.points == 2:
            bonus = -1
        elif self.points == 3:
            bonus = 0
        else:
            bonus = self.points - 3
        if len(self._base_attributes) != 1:
            raise ValueError("Use resolve_multi_attribute_skill for multi-attribute skills.")
        return attributes[self._base_attributes[0]] + bonus

    _base_attributes: tuple[str, ...] = field(default_factory=tuple, repr=False)


def resolve_skill_value(
    *,
    points: int,
    attribute_values: tuple[int, ...],
    untrained_penalty: int | None = None,
) -> int:
    """Resolve the confirmed investment table without guessing multi-attribute rules."""
    if points < 0:
        raise ValueError("Skill points cannot be negative.")
    if not attribute_values:
        raise ValueError("At least one base attribute is required.")

    if points == 0:
        if untrained_penalty is None:
            raise ValueError("The source-specific untrained penalty must be supplied.")
        return max(attribute_values) + untrained_penalty

    bonus_by_points = {
        1: -2,
        2: -1,
        3: 0,
        4: 1,
        5: 2,
    }
    if points not in bonus_by_points:
        # The source's table continues conceptually, but this prototype
        # does not assume values beyond the documented table.
        raise ValueError("Skill-point value is outside the currently documented table.")

    return max(attribute_values) + bonus_by_points[points]
