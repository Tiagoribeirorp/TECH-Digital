"""Configurable combat parameters for T.E.C.H. Digital.

Values marked provisional are development placeholders, not canon rules.
When the author validates a rule, change the value here (or replace the
parameter with the official formula) without rewriting the combat engine.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CombatRules:
    # PROVISIONAL: the source does not yet define these universal formulas.
    default_attack_value: int = 10
    default_defense_value: int = 10
    default_damage: int = 5

    # Placeholder only: future rules can replace these with formulas.

    # CONFIRMED values from the current combat material.
    surgical_attack_bonus: int = 3
    surgical_damage_bonus: int = 3
    defensive_fight_attack_modifier: int = -3
    defensive_fight_defense_modifier: int = 1
    defensive_stance_defense_bonus: int = 4
    dodge_speed_cost: float = 3
    block_speed_cost: float = 3
    movement_per_speed: float = 1.5
    dedicated_move_distance: float = 3.0


DEFAULT_COMBAT_RULES = CombatRules()
