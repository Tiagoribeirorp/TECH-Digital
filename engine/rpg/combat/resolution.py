"""Combat resolution primitives.

These functions resolve only rules whose inputs are already known. They do not
invent an attack-vs-defense formula or a damage formula that is still pending
validation in the source material.
"""

from dataclasses import dataclass

from engine.rpg.core.tests import TestResult, resolve_test
from engine.rpg.combat.actions import CombatAction, action_modifiers
from engine.rpg.combat.equipment_values import weapon_damage, weapon_speed
from engine.rpg.combat.state import CombatantState


@dataclass(frozen=True)
class AttackResolution:
    test: TestResult
    attack_modifier: int
    effective_attack_value: int


@dataclass(frozen=True)
class ActionAttackResolution:
    action: CombatAction
    attack: AttackResolution
    base_damage: int | None
    final_damage: int | None
    weapon_speed: float | None


def resolve_attack_action(
    *,
    action: CombatAction,
    roll: int,
    attack_value: int,
    combatant: CombatantState,
    base_damage: int | None = None,
) -> ActionAttackResolution:
    """Resolve confirmed action modifiers around an attack test.

    The attack target value and base damage formula remain external because the
    source does not yet define a universal attack-vs-defense or damage formula.
    If no base damage is supplied, an explicitly defined weapon damage is used.
    """
    modifiers = action_modifiers(action)
    attack = resolve_attack_test(
        roll=roll,
        attack_value=attack_value,
        attack_modifier=modifiers["attack"],
    )
    resolved_base_damage = base_damage
    if resolved_base_damage is None:
        resolved_base_damage = weapon_damage(combatant.equipped_combat_equipment)
    if resolved_base_damage is not None and resolved_base_damage < 0:
        raise ValueError("Damage cannot be negative")
    final_damage = None if resolved_base_damage is None else resolved_base_damage + modifiers["damage"]
    return ActionAttackResolution(
        action=action,
        attack=attack,
        base_damage=resolved_base_damage,
        final_damage=final_damage,
        weapon_speed=weapon_speed(
            combatant.equipped_combat_equipment,
            surgical=action is CombatAction.SURGICAL_ATTACK,
        ),
    )


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
