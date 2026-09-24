import unittest

from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.core.tests import resolve_resisted_test, resolve_test


class CharacterStateTests(unittest.TestCase):
    def setUp(self):
        self.character = CharacterState(
            id="test-001",
            name="Test",
            race_id="human",
            attributes=Attributes(
                strength=10,
                reflexes=12,
                health=14,
                perception=16,
                intelligence=11,
                willpower=13,
                charisma=9,
            ),
            skill_values={"furtividade": 12},
        )

    def test_confirmed_derived_stats(self):
        stats = self.character.derive_stats()
        self.assertEqual(stats.reaction, 9)
        self.assertEqual(stats.senses, 16)
        self.assertEqual(stats.hp_max, 14)
        self.assertEqual(stats.fatigue_max, 13)
        self.assertEqual(stats.evasion, 7)
        self.assertEqual(stats.speed_per_turn, 6)

    def test_resources_initialize_from_derived_stats(self):
        self.character.initialize_resources()
        self.assertEqual(self.character.current_hp, 14)
        self.assertEqual(self.character.current_fatigue, 13)

    def test_skill_modifier_is_applied_directly(self):
        self.assertEqual(self.character.effective_skill("furtividade", -2), 10)


class ResolutionTests(unittest.TestCase):
    def test_d20_success_is_less_than_or_equal(self):
        result = resolve_test(10, 10)
        self.assertTrue(result.success)
        self.assertEqual(result.margin, 0)

    def test_d20_failure_is_greater(self):
        result = resolve_test(11, 10)
        self.assertFalse(result.success)
        self.assertEqual(result.margin, -1)

    def test_natural_one_is_recorded(self):
        self.assertTrue(resolve_test(1, 1).critical_success)

    def test_resisted_test_uses_margin(self):
        first = resolve_test(8, 12)  # margin 4
        second = resolve_test(9, 11)  # margin 2
        self.assertEqual(resolve_resisted_test(first, second), 1)


if __name__ == "__main__":
    unittest.main()
