import unittest

from engine.rpg.combat.actions import (
    ACTION_RULES,
    CombatAction,
    can_pay_speed,
    dedicated_move_distance,
    movement_distance_for_speed,
)


class CombatActionRuleTests(unittest.TestCase):
    def test_surgical_attack_modifiers_are_confirmed_values(self):
        rule = ACTION_RULES[CombatAction.SURGICAL_ATTACK]
        self.assertEqual(rule.attack_modifier, 3)
        self.assertEqual(rule.damage_modifier, 3)

    def test_fight_defensively_modifiers_are_confirmed_values(self):
        rule = ACTION_RULES[CombatAction.FIGHT_DEFENSIVELY]
        self.assertEqual(rule.attack_modifier, -3)
        self.assertEqual(rule.defense_modifier, 1)

    def test_defensive_stance_gives_four_defense(self):
        self.assertEqual(
            ACTION_RULES[CombatAction.DEFENSIVE_STANCE].defense_modifier,
            4,
        )

    def test_confirmed_movement_ratio(self):
        self.assertEqual(movement_distance_for_speed(6), 9)
        self.assertEqual(dedicated_move_distance(), 3)

    def test_speed_cost_validation(self):
        self.assertTrue(can_pay_speed(3, 3))
        self.assertFalse(can_pay_speed(2, 3))
        with self.assertRaises(ValueError):
            can_pay_speed(3, -1)


if __name__ == "__main__":
    unittest.main()
