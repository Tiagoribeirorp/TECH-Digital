"""Resolution helpers for basic non-attack combat actions.

Only confirmed mechanical costs/effects are applied here. Defensive actions
record the selected defense mode; the final attack-vs-defense interaction stays
in the opposed attack layer until the source defines the complete formula.
"""

from dataclasses import dataclass

from engine.rpg.combat.actions import (
    CombatAction,
    action_speed_cost,
    dedicated_move_distance,
    movement_distance_for_speed,
)
from engine.rpg.combat.state import CombatPhase, CombatState
from engine.rpg.core.resolution import ResolutionRecord
from engine.rpg.core.resolution_log import append_resolution


@dataclass(frozen=True)
class ActionExecutionResult:
    action: CombatAction
    character_id: str
    speed_spent: float
    distance_moved: float
    defense_mode: str | None
    resolution_id: str
    resolution_sequence: int


def execute_move(
    combat: CombatState,
    character_id: str,
    *,
    dedicated: bool = True,
) -> ActionExecutionResult:
    if combat.phase != CombatPhase.EXECUTION:
        raise ValueError("Actions can only resolve during execution phase")
    combatant = combat.get_combatant(character_id)
    if not combatant.is_active:
        raise ValueError("Inactive combatant cannot move")

    if dedicated:
        distance = dedicated_move_distance()
        speed_spent = 0.0
    else:
        speed_spent = combatant.available_speed
        distance = movement_distance_for_speed(speed_spent)

    combatant.available_speed -= speed_spent
    record = append_resolution(
        combat.resolution_log,
        ResolutionRecord(
            source="combat",
            action=CombatAction.MOVE.value,
            actor_id=character_id,
            result="moved",
            consequences={
                "distance_m": distance,
                "speed_spent": speed_spent,
            },
        ),
    )
    combat.combat_log.append({
        "event": "movement_resolved",
        "round": combat.round_number,
        "character_id": character_id,
        "distance_m": distance,
        "speed_spent": speed_spent,
    })
    return ActionExecutionResult(
        action=CombatAction.MOVE,
        character_id=character_id,
        speed_spent=speed_spent,
        distance_moved=distance,
        defense_mode=None,
        resolution_id=record.id,
        resolution_sequence=record.sequence,
    )


def execute_defensive_action(
    combat: CombatState,
    character_id: str,
    action: CombatAction,
    *,
    weapon_speed: float | None = None,
) -> ActionExecutionResult:
    if combat.phase != CombatPhase.EXECUTION:
        raise ValueError("Actions can only resolve during execution phase")
    if action not in {
        CombatAction.DODGE,
        CombatAction.PARRY,
        CombatAction.BLOCK,
    }:
        raise ValueError("Action is not a basic defensive action")

    combatant = combat.get_combatant(character_id)
    if not combatant.is_active:
        raise ValueError("Inactive combatant cannot defend")

    cost = action_speed_cost(action, weapon_speed=weapon_speed)
    if combatant.available_speed < cost:
        raise ValueError("Not enough Vel/Tur for defensive action")
    combatant.available_speed -= cost

    defense_mode = {
        CombatAction.DODGE: "dodge",
        CombatAction.PARRY: "parry",
        CombatAction.BLOCK: "block",
    }[action]
    combatant.declared_action = action.value

    record = append_resolution(
        combat.resolution_log,
        ResolutionRecord(
            source="combat",
            action=action.value,
            actor_id=character_id,
            result="defense_declared",
            consequences={
                "defense_mode": defense_mode,
                "speed_spent": cost,
            },
        ),
    )
    combat.combat_log.append({
        "event": "defense_declared",
        "round": combat.round_number,
        "character_id": character_id,
        "action": action.value,
        "defense_mode": defense_mode,
        "speed_spent": cost,
    })
    return ActionExecutionResult(
        action=action,
        character_id=character_id,
        speed_spent=cost,
        distance_moved=0.0,
        defense_mode=defense_mode,
        resolution_id=record.id,
        resolution_sequence=record.sequence,
    )
