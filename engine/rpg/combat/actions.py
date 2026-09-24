"""Combat action definitions and confirmed costs/modifiers.

Only rules explicitly established in the project are encoded here. Attack/defense
resolution formulas remain outside this module until the source material validates them.
"""

from dataclasses import dataclass
from enum import Enum


class CombatAction(str, Enum):
    ATTACK = "attack"
    MOVE = "move"
    SURGICAL_ATTACK = "surgical_attack"
    FIGHT_DEFENSIVELY = "fight_defensively"
    CHANGE_ACTION = "change_action"
    MULTIPLE_ATTACK = "multiple_attack"
    DEFENSIVE_STANCE = "defensive_stance"
    DISARM = "disarm"
    IMMOBILIZE = "immobilize"
    DODGE = "dodge"
    PARRY = "parry"
    BLOCK = "block"
    CHARGING = "charging"


@dataclass(frozen=True)
class ActionRule:
    action: CombatAction
    speed_cost: float = 0.0
    attack_modifier: int = 0
    defense_modifier: int = 0
    damage_modifier: int = 0
    description: str = ""


# Confirmed values from the combat specification.
ACTION_RULES: dict[CombatAction, ActionRule] = {
    CombatAction.ATTACK: ActionRule(
        CombatAction.ATTACK,
        description="Ataque básico; resolução depende dos valores de combate validados.",
    ),
    CombatAction.MOVE: ActionRule(
        CombatAction.MOVE,
        speed_cost=0.0,
        description="Ação dedicada a movimento; a distância confirmada é 3m.",
    ),
    CombatAction.SURGICAL_ATTACK: ActionRule(
        CombatAction.SURGICAL_ATTACK,
        attack_modifier=3,
        damage_modifier=3,
        description="Dobra a velocidade da arma; +3 acerto e +3 dano.",
    ),
    CombatAction.FIGHT_DEFENSIVELY: ActionRule(
        CombatAction.FIGHT_DEFENSIVELY,
        attack_modifier=-3,
        defense_modifier=1,
        description="+1 Defesa e -3 ataque.",
    ),
    CombatAction.DEFENSIVE_STANCE: ActionRule(
        CombatAction.DEFENSIVE_STANCE,
        defense_modifier=4,
        description="+4 Defesa até a próxima vez.",
    ),
    CombatAction.DODGE: ActionRule(
        CombatAction.DODGE,
        speed_cost=3,
        description="Esquiva anunciada antes; custo de 3 Vel/Tur.",
    ),
    CombatAction.BLOCK: ActionRule(
        CombatAction.BLOCK,
        speed_cost=3,
        description="Bloqueio; custo de 3 Vel/Tur.",
    ),
}


def action_modifiers(action: CombatAction) -> dict[str, int]:
    """Return confirmed numeric modifiers for a combat action.

    These values are currently encoded as source-confirmed action rules;
    universal attack/defense formulas remain configurable elsewhere.
    """
    rule = ACTION_RULES[action]
    return {
        "attack": rule.attack_modifier,
        "defense": rule.defense_modifier,
        "damage": rule.damage_modifier,
    }


def movement_distance_for_speed(speed_per_turn: float) -> float:
    """Convert Vel/Tur into metres using the confirmed 1.5m ratio."""
    return speed_per_turn * 1.5


def dedicated_move_distance() -> float:
    """Distance for an action dedicated only to movement."""
    return 3.0


def action_speed_cost(action: CombatAction, *, weapon_speed: float | None = None) -> float:
    """Return the confirmed speed cost, including Parry weapon speed."""
    rule = ACTION_RULES[action]
    if action is CombatAction.PARRY:
        if weapon_speed is None:
            raise ValueError("Parry requires the weapon speed")
        if weapon_speed < 0:
            raise ValueError("Weapon speed cannot be negative")
        return weapon_speed
    return rule.speed_cost


def can_pay_speed(current_speed: float, cost: float) -> bool:
    if cost < 0:
        raise ValueError("Speed cost cannot be negative")
    return current_speed >= cost
