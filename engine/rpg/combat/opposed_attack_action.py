"""Apply opposed attack resolution to a live CombatState.

Attack and defense values remain explicit inputs because the source does not
establish a universal formula deriving them from every weapon, armor and skill.
"""

from dataclasses import dataclass

from engine.rpg.combat.actions import CombatAction, action_modifiers
from engine.rpg.combat.rules import CombatRules, DEFAULT_COMBAT_RULES
from engine.rpg.combat.damage import apply_damage
from engine.rpg.combat.opposed_attack import (
    OpposedAttackResolution,
    resolve_opposed_attack,
)
from engine.rpg.combat.state import CombatPhase, CombatState
from engine.rpg.core.resolution import ResolutionRecord
from engine.rpg.core.resolution_log import append_resolution


@dataclass(frozen=True)
class OpposedAttackCombatResult:
    resolution: OpposedAttackResolution
    damage_applied: int
    target_hp: int
    target_status: str
    resolution_id: str
    resolution_sequence: int


def resolve_opposed_attack_action(
    combat: CombatState,
    attacker_id: str,
    target_id: str,
    *,
    attack_roll: int,
    attack_value: int,
    defense_roll: int,
    defense_value: int,
    damage: int,
    action: CombatAction = CombatAction.ATTACK,
    rules: CombatRules = DEFAULT_COMBAT_RULES,
) -> OpposedAttackCombatResult:
    if combat.phase != CombatPhase.EXECUTION:
        raise ValueError("Attacks can only resolve during execution phase")

    attacker = combat.get_combatant(attacker_id)
    target = combat.get_combatant(target_id)
    if not attacker.is_active:
        raise ValueError("Inactive attacker cannot attack")
    if not target.is_active:
        raise ValueError("Inactive target cannot be attacked")
    if damage < 0:
        raise ValueError("Damage cannot be negative")

    modifiers = action_modifiers(action)
    effective_attack = attack_value + modifiers["attack"]
    effective_defense = defense_value + modifiers["defense"]
    effective_damage = max(0, damage + modifiers["damage"])

    resolution = resolve_opposed_attack(
        attack_roll=attack_roll,
        attack_value=effective_attack,
        defense_roll=defense_roll,
        defense_value=effective_defense,
        damage=effective_damage,
    )

    damage_result = apply_damage(
        target.current_hp,
        effective_damage if resolution.damage_applies else 0,
    )
    target.current_hp = damage_result.remaining_hp
    if damage_result.became_unconscious:
        target.status = "unconscious"

    outcome = "attacker_wins" if resolution.attacker_wins else "defender_wins_or_tied"
    combat.combat_log.append({
        "event": "opposed_attack_resolved",
        "round": combat.round_number,
        "action": action.value,
        "attacker_id": attacker_id,
        "target_id": target_id,
        "attack_roll": attack_roll,
        "attack_value": effective_attack,
        "defense_roll": defense_roll,
        "defense_value": effective_defense,
        "attack_margin": resolution.attack.margin,
        "defense_margin": resolution.defense.margin,
        "margin_difference": resolution.margin_difference,
        "outcome": outcome,
        "damage": damage_result.applied_damage,
        "target_hp": target.current_hp,
        "target_status": target.status,
    })

    record = append_resolution(
        combat.resolution_log,
        ResolutionRecord(
            source="combat",
            action=action.value,
            actor_id=attacker_id,
            target_id=target_id,
            random_roll=attack_roll,
            modifiers=modifiers,
            effective_value=effective_attack,
            result=outcome,
            consequences={
                "attack_roll": attack_roll,
                "defense_roll": defense_roll,
                "attack_value": effective_attack,
                "defense_value": effective_defense,
                "attack_margin": resolution.attack.margin,
                "defense_margin": resolution.defense.margin,
                "damage": damage_result.applied_damage,
                "target_hp": target.current_hp,
                "target_status": target.status,
            },
        ),
    )

    return OpposedAttackCombatResult(
        resolution=resolution,
        damage_applied=damage_result.applied_damage,
        target_hp=target.current_hp,
        target_status=target.status,
        resolution_id=record.id,
        resolution_sequence=record.sequence,
    )
