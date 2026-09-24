"""Apply opposed attack resolution to a live CombatState.

Attack and defense values remain explicit inputs because the source does not
establish a universal formula deriving them from every weapon, armor and skill.
"""

from dataclasses import dataclass

from engine.rpg.combat.actions import CombatAction, action_modifiers
from engine.rpg.combat.defense import DefenseMode, resolve_defense
from engine.rpg.combat.defensive_state import DefenseChoice
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
    attack_value: int | None = None,
    defense_roll: int,
    defense_value: int | None = None,
    damage: int | None = None,
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
    base_attack = rules.default_attack_value if attack_value is None else attack_value
    base_defense = rules.default_defense_value if defense_value is None else defense_value
    base_damage = rules.default_damage if damage is None else damage
    if base_damage < 0:
        raise ValueError("Damage cannot be negative")

    modifiers = action_modifiers(action)
    effective_attack = base_attack + modifiers["attack"]
    effective_defense = base_defense + modifiers["defense"]
    effective_damage = max(0, base_damage + modifiers["damage"])

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



def resolve_attack_against_choice(
    combat: CombatState,
    attacker_id: str,
    target_id: str,
    *,
    attack_roll: int,
    defense_roll: int,
    roller=None,
    attack_value: int | None = None,
    defense_value: int | None = None,
    damage: int | None = None,
    action: CombatAction = CombatAction.ATTACK,
    rules: CombatRules = DEFAULT_COMBAT_RULES,
) -> OpposedAttackCombatResult:
    """Resolve an attack using the target's stored defensive choice.

    The choice selects the already-defined defense type and cost. The caller
    may still provide an explicit defense value until the final attack/defense
    formulas are validated by the source.
    """
    target = combat.get_combatant(target_id)
    choice = target.defense_choice.choice
    if choice is DefenseChoice.NONE:
        selected_defense = defense_value
    else:
        mode = {
            DefenseChoice.DODGE: DefenseMode.DODGE,
            DefenseChoice.PARRY: DefenseMode.PARRY,
            DefenseChoice.BLOCK: DefenseMode.BLOCK,
        }[choice]
        selected_defense = defense_value
        if selected_defense is None:
            if mode is DefenseMode.PARRY:
                skill = target.character.skill_values.get("parry")
                if skill is None:
                    raise ValueError("Parry requires an explicit defense value or parry skill")
                selected_defense = resolve_defense(
                    target.character,
                    mode,
                    parry_skill=skill,
                    equipment=target.equipped_combat_equipment,
                ).value
            elif mode is DefenseMode.BLOCK:
                skill = target.character.skill_values.get("shield")
                if skill is None:
                    raise ValueError("Block requires an explicit defense value or shield skill")
                selected_defense = resolve_defense(
                    target.character,
                    mode,
                    shield_skill=skill,
                    equipment=target.equipped_combat_equipment,
                ).value
            else:
                selected_defense = resolve_defense(target.character, mode).value

    return resolve_opposed_attack_action(
        combat,
        attacker_id,
        target_id,
        attack_roll=attack_roll,
        attack_value=attack_value,
        defense_roll=defense_roll,
        defense_value=selected_defense,
        damage=damage,
        action=action,
        rules=rules,
    )


def perform_basic_attack(
    combat: CombatState,
    attacker_id: str,
    target_id: str,
    *,
    roller,
    attack_value: int | None = None,
    defense_value: int | None = None,
    damage: int | None = None,
    rules: CombatRules = DEFAULT_COMBAT_RULES,
) -> OpposedAttackCombatResult:
    """Perform one basic attack using provisional defaults when unspecified."""
    attacker = combat.get_combatant(attacker_id)
    weapon = attacker.equipped_combat_equipment.weapon
    weapon_damage = None if weapon is None else weapon.damage
    base_damage = damage if damage is not None else weapon_damage
    if base_damage is None:
        base_damage = rules.default_damage

    if not attacker.is_active:
        raise ValueError("Inactive attacker cannot attack")
    if not can_pay_basic_attack_speed(attacker.available_speed):
        raise ValueError("Not enough Vel/Tur for basic attack")

    result = resolve_opposed_attack_action(
        combat,
        attacker_id,
        target_id,
        attack_roll=roller(),
        attack_value=attack_value,
        defense_roll=roller(),
        defense_value=defense_value,
        damage=base_damage,
        rules=rules,
    )
    attacker.available_speed -= 0
    return result


def can_pay_basic_attack_speed(available_speed: float) -> bool:
    """Basic attack currently has no confirmed Vel/Tur cost."""
    return available_speed >= 0
