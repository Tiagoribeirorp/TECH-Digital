"""Regression checks for the first combat balance pass."""

import unittest

from engine.rpg.bridge import ENEMY_PROFILES, execute_combat_action


class CombatBalanceTests(unittest.TestCase):
    def test_raider_is_tougher_than_training_dummy(self) -> None:
        dummy = ENEMY_PROFILES["training_dummy"]
        raider = ENEMY_PROFILES["raider"]

        self.assertGreater(raider["health"], dummy["health"])
        self.assertGreater(raider["attack_damage"], dummy["attack_damage"])
        self.assertGreaterEqual(raider["attack_target"], dummy["attack_target"])

    def test_standard_attack_and_special_have_distinct_costs(self) -> None:
        normal = execute_combat_action(
            action="attack",
            current_hp=12,
            current_fatigue=12,
            enemy_hp=10,
            forced_roll=10,
        )
        special = execute_combat_action(
            action="special",
            current_hp=12,
            current_fatigue=12,
            enemy_hp=10,
            forced_roll=10,
        )

        self.assertGreater(special["damage"], normal["damage"])
        self.assertLess(special["fatigue"], normal["fatigue"])

    def test_recovery_is_limited_by_fatigue_maximum(self) -> None:
        result = execute_combat_action(
            action="recover",
            current_hp=12,
            current_fatigue=11,
            enemy_hp=10,
        )

        self.assertEqual(result["fatigue"], result["fatigue_max"])
        self.assertEqual(result["fatigue_recovered"], 1)


if __name__ == "__main__":
    unittest.main()
