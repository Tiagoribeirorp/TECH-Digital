"""Live opposed-attack resolution using the authoritative d20 roller.

This module bridges combat decisions to the core test resolver. It deliberately
does not invent attack or defense formulas: callers provide the effective
values when those rules are not yet confirmed.
"""

from engine.rpg.combat.actions import CombatAction
from engine.rpg.combat.opposed_attack_action import (
    OpposedAttackCombatResult,
    resolve_attack_against_choice,
)
from engine.rpg.combat.rules import CombatRules, DEFAULT_COMBAT_RULES
from engine.rpg.combat.state import CombatState
from engine.rpg.core.dice import DiceRoller, roll_d20


def resolve_live_attack_against_choice(
    combat: CombatState,
    attacker_id: str,
    target_id: str,
    *,
    roller: DiceRoller | None = None,
    attack_value: int | None = None,
    defense_value: int | None = None,
    damage: int | None = None,
    action: CombatAction = CombatAction.ATTACK,
    rules: CombatRules = DEFAULT_COMBAT_RULES,
) -> OpposedAttackCombatResult:
    """Roll both combat tests through the authoritative engine roller.

    The returned combat result contains the mechanical outcome. A presentation
    layer can animate the two recorded rolls after this function returns.
    """
    attack_roll = roll_d20(roller)
    defense_roll = roll_d20(roller)

    return resolve_attack_against_choice(
        combat,
        attacker_id,
        target_id,
        attack_roll=attack_roll,
        defense_roll=defense_roll,
        attack_value=attack_value,
        defense_value=defense_value,
        damage=damage,
        action=action,
        rules=rules,
    )
