"""Generic opposed attack resolution for T.E.C.H. Digital.

The source establishes resisted tests by margin. It does not establish a single
universal attack skill or a universal formula for deriving defense from every
weapon/armor combination, so those values remain explicit inputs here.
"""

from dataclasses import dataclass

from engine.rpg.core.tests import resolve_resisted_test, TestResult


@dataclass(frozen=True)
class OpposedAttackResolution:
    attack: TestResult
    defense: TestResult
    attacker_wins: bool
    margin_difference: int
    damage_applies: bool


def resolve_opposed_attack(
    *,
    attack_roll: int,
    attack_value: int,
    defense_roll: int,
    defense_value: int,
    damage: int,
) -> OpposedAttackResolution:
    if damage < 0:
        raise ValueError("Damage cannot be negative")

    attack, defense = resolve_resisted_test(
        first_roll=attack_roll,
        first_value=attack_value,
        second_roll=defense_roll,
        second_value=defense_value,
    )

    attacker_wins = attack.margin > defense.margin
    return OpposedAttackResolution(
        attack=attack,
        defense=defense,
        attacker_wins=attacker_wins,
        margin_difference=attack.margin - defense.margin,
        damage_applies=attacker_wins and damage > 0,
    )
