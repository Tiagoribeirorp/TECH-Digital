"""Focused bridge tests for the first playable combat loop."""

import unittest
from unittest.mock import patch

from engine.rpg.bridge import execute_combat_action, roll_combat_initiative


class BridgeCombatTests(unittest.TestCase):
    def test_initiative_orders_highest_roll_first(self) -> None:
        result = roll_combat_initiative(hero_roll=17, enemy_roll=9)

        self.assertEqual(result["first"], "hero")
        self.assertEqual(result["order"], ["hero", "enemy"])

    def test_initiative_breaks_ties_in_favor_of_hero(self) -> None:
        result = roll_combat_initiative(hero_roll=12, enemy_roll=12)

        self.assertEqual(result["first"], "hero")

    def test_attack_hit_applies_damage_and_fatigue(self) -> None:
        result = execute_combat_action(
            action="attack",
            current_hp=12,
            current_fatigue=12,
            enemy_hp=10,
            forced_roll=10,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["damage"], 5)
        self.assertEqual(result["enemy_hp_after_player_action"], 5)
        self.assertEqual(result["fatigue"], 10)

    def test_defend_reduces_enemy_target(self) -> None:
        result = execute_combat_action(
            action="defend",
            current_hp=12,
            current_fatigue=12,
            enemy_hp=10,
        )

        self.assertEqual(result["defense_bonus"], 4)
        self.assertEqual(result["enemy_target"], 6)
        self.assertEqual(result["fatigue"], 11)

    def test_special_attack_uses_extra_damage_and_fatigue(self) -> None:
        result = execute_combat_action(
            action="special",
            current_hp=12,
            current_fatigue=12,
            enemy_hp=10,
            forced_roll=10,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["damage"], 8)
        self.assertEqual(result["enemy_hp_after_player_action"], 2)
        self.assertEqual(result["fatigue"], 9)

    def test_attack_can_finish_combat_without_enemy_response(self) -> None:
        result = execute_combat_action(
            action="attack",
            current_hp=12,
            current_fatigue=12,
            enemy_hp=5,
            forced_roll=1,
        )

        self.assertEqual(result["phase"], "finished")
        self.assertFalse(result["enemy_active"])
        self.assertIsNone(result["enemy_roll"])

    def test_action_is_blocked_without_fatigue(self) -> None:
        result = execute_combat_action(
            action="attack",
            current_hp=12,
            current_fatigue=1,
            enemy_hp=10,
        )

        self.assertEqual(result["phase"], "blocked")
        self.assertEqual(result["reason"], "not_enough_fatigue")

    def test_recover_restores_fatigue_without_exceeding_maximum(self) -> None:
        result = execute_combat_action(
            action="recover",
            current_hp=12,
            current_fatigue=10,
            enemy_hp=10,
        )

        self.assertEqual(result["fatigue_recovered"], 2)
        self.assertEqual(result["fatigue"], 12)

    def test_enemy_can_finish_combat(self) -> None:
        with patch("engine.rpg.bridge.roll_d20", return_value=1):
            result = execute_combat_action(
                action="attack",
                current_hp=3,
                current_fatigue=12,
                enemy_hp=10,
                forced_roll=20,
            )

        self.assertEqual(result["phase"], "finished")
        self.assertFalse(result["hero_active"])
        self.assertEqual(result["hp"], 0)


if __name__ == "__main__":
    unittest.main()
