"""Combat resolution primitives.

These functions resolve only rules whose inputs are already known. They do not
invent an attack-vs-defense formula or a damage formula that is still pending
validation in the source material.
"""

from dataclasses import dataclass

from engine.rpg.core.tests import TestResult, resolve_test


@dataclass(frozen=True)
class AttackResolution:
    test: TestResult
    attack_modifier: int
    effective_attack_value: int


def resolve_attack_test(
    *,
    roll: int,
    attack_value: int,
    attack_modifier: int = 0,
) -> AttackResolution:
    """Resolve an attack d20 test against an already-established target value."""
    effective_value = attack_value + attack_modifier
    test = resolve_test(roll, effective_value)
    return AttackResolution(
        test=test,
        attack_modifier=attack_modifier,
        effective_attack_value=effective_value,
    )
