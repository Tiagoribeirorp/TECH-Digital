"""Tests for basic non-attack combat actions."""

from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.basic_actions import execute_defensive_action, execute_move
from engine.rpg.combat.actions import CombatAction
from engine.rpg.combat.state import CombatPhase, CombatState, CombatantState


def _combat():
    a = CharacterState(
        id="a", name="A", race_id="prototype",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )
    b = CharacterState(
        id="b", name="B", race_id="prototype",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )
    return CombatState(
        participants=[CombatantState.from_character(a), CombatantState.from_character(b)],
        phase=CombatPhase.EXECUTION,
        round_number=1,
        status="active",
    )


def test_dedicated_move_records_three_metres():
    combat = _combat()
    result = execute_move(combat, "a", dedicated=True)

    assert result.distance_moved == 3.0
    assert result.speed_spent == 0.0
    assert len(combat.resolution_log) == 1


def test_dodge_consumes_three_speed():
    combat = _combat()
    before = combat.get_combatant("a").available_speed
    result = execute_defensive_action(combat, "a", CombatAction.DODGE)

    assert result.speed_spent == 3
    assert combat.get_combatant("a").available_speed == before - 3


def test_parry_consumes_weapon_speed():
    combat = _combat()
    before = combat.get_combatant("a").available_speed
    result = execute_defensive_action(
        combat, "a", CombatAction.PARRY, weapon_speed=3
    )

    assert result.speed_spent == 3
    assert combat.get_combatant("a").available_speed == before - 3
