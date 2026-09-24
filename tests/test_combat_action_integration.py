import unittest

from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.engine import (
    begin_execution,
    can_execute_action,
    finish_round,
    roll_initiative,
    spend_action_speed,
    start_combat,
)
from engine.rpg.combat.actions import CombatAction


def character(cid: str) -> CharacterState:
    return CharacterState(
        id=cid, name=cid, race_id="test",
        attributes=Attributes(10, 12, 10, 10, 10, 10, 10),
    )


class CombatActionIntegrationTests(unittest.TestCase):
    def test_dodge_costs_three_speed(self):
        combat = start_combat([character("a"), character("b")])
        roll_initiative(combat, iter([10, 10]).__next__)
        begin_execution(combat)
        self.assertTrue(can_execute_action(combat, "a", CombatAction.DODGE))
        spend_action_speed(combat, "a", CombatAction.DODGE)
        self.assertEqual(combat.get_combatant("a").available_speed, 3)

    def test_block_cannot_be_paid_if_less_than_three_speed(self):
        combat = start_combat([character("a"), character("b")])
        roll_initiative(combat, iter([10, 10]).__next__)
        begin_execution(combat)
        combat.get_combatant("a").available_speed = 2
        self.assertFalse(can_execute_action(combat, "a", CombatAction.BLOCK))


if __name__ == "__main__":
    unittest.main()
