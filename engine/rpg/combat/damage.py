"""Damage application primitives.

Damage magnitude remains an explicit input until the source validates the
weapon/damage formula. This module owns only the confirmed HP state changes.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DamageResult:
    requested_damage: int
    applied_damage: int
    remaining_hp: int
    became_unconscious: bool


def apply_damage(current_hp: int, damage: int) -> DamageResult:
    if current_hp < 0:
        raise ValueError("Current HP cannot be negative")
    if damage < 0:
        raise ValueError("Damage cannot be negative")

    applied = min(current_hp, damage)
    remaining = current_hp - applied

    return DamageResult(
        requested_damage=damage,
        applied_damage=applied,
        remaining_hp=remaining,
        became_unconscious=remaining == 0,
    )
