"""Combat flow orchestration for the T.E.C.H. Digital RPG Engine prototype."""

from collections.abc import Callable, Iterable

from engine.rpg.character.state import CharacterState
from engine.rpg.combat.actions import ACTION_RULES, CombatAction, can_pay_speed
from engine.rpg.combat.state import CombatPhase, CombatState, CombatantState

Roller = Callable[[], int]


def start_combat(characters: Iterable[CharacterState]) -> CombatState:
    participants = [CombatantState.from_character(character) for character in characters]
    if len(participants) < 2:
        raise ValueError("Combat requires at least two participants")
    return CombatState(participants=participants, status="active")


def roll_initiative(combat: CombatState, roller: Roller) -> list[str]:
    if combat.status != "active":
        raise ValueError("Combat is not active")
    for combatant in combat.participants:
        roll = roller()
        if not 1 <= roll <= 20:
            raise ValueError("initiative d20 roll must be between 1 and 20")
        combatant.initiative_result = combatant.effective_stats().reaction_time_base + roll
    ordered = sorted(combat.participants, key=lambda item: item.initiative_result or -1, reverse=True)
    combat.initiative_order = [item.character.id for item in ordered]
    combat.round_number = 1
    combat.phase = CombatPhase.DECLARATION
    combat.combat_log.append({"event": "initiative_resolved", "round": 1, "order": list(combat.initiative_order)})
    return combat.initiative_order


def declaration_order(combat: CombatState) -> list[str]:
    if not combat.initiative_order:
        raise ValueError("Initiative must be resolved before declaration")
    return list(reversed(combat.initiative_order))


def execution_order(combat: CombatState) -> list[str]:
    if not combat.initiative_order:
        raise ValueError("Initiative must be resolved before execution")
    return list(combat.initiative_order)


def declare_action(combat: CombatState, character_id: str, action: str) -> None:
    if combat.phase != CombatPhase.DECLARATION:
        raise ValueError("Actions can only be declared during declaration phase")
    combat.get_combatant(character_id).declared_action = action
    combat.combat_log.append({"event": "action_declared", "round": combat.round_number,
                              "character_id": character_id, "action": action})


def begin_execution(combat: CombatState) -> list[str]:
    if combat.phase != CombatPhase.DECLARATION:
        raise ValueError("Combat is not awaiting execution")
    combat.phase = CombatPhase.EXECUTION
    return execution_order(combat)


def action_rule(action: CombatAction):
    return ACTION_RULES[action]


def can_execute_action(combat: CombatState, character_id: str, action: CombatAction) -> bool:
    combatant = combat.get_combatant(character_id)
    return can_pay_speed(combatant.available_speed, action_rule(action).speed_cost)


def spend_action_speed(combat: CombatState, character_id: str, action: CombatAction) -> None:
    combatant = combat.get_combatant(character_id)
    rule = action_rule(action)
    if not can_pay_speed(combatant.available_speed, rule.speed_cost):
        raise ValueError("Not enough Vel/Tur for action")
    combatant.available_speed -= rule.speed_cost


def resolve_basic_attack(combat: CombatState, attacker_id: str, target_id: str,
                         *, attack_success: bool, damage: int = 0) -> dict[str, object]:
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
    applied_damage = damage if attack_success else 0
    target.current_hp = max(0, target.current_hp - applied_damage)
    if target.current_hp == 0:
        target.status = "unconscious"
    result = {"event": "basic_attack_resolved", "round": combat.round_number,
              "attacker_id": attacker_id, "target_id": target_id,
              "success": attack_success, "damage": applied_damage,
              "target_hp": target.current_hp}
    combat.combat_log.append(result)
    return result


def finish_round(combat: CombatState) -> None:
    if combat.phase != CombatPhase.EXECUTION:
        raise ValueError("Round can only finish after execution")
    active = [item for item in combat.participants if item.is_active]
    if len(active) <= 1:
        combat.status = "finished"
        combat.phase = CombatPhase.FINISHED
        combat.combat_log.append({"event": "combat_finished", "round": combat.round_number})
        return
    for combatant in combat.participants:
        combatant.declared_action = None
        combatant.available_speed = combatant.effective_stats().speed_per_turn
    combat.round_number += 1
    combat.phase = CombatPhase.DECLARATION
    combat.combat_log.append({"event": "round_started", "round": combat.round_number})
