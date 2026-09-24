import unittest

from engine.rpg.equipment.definitions import (
    EquipmentCategory,
    EXOSKELETON,
    FULL_EXOSKELETON,
    InventoryState,
    LoadCategory,
    WeaponDefinition,
)
from engine.rpg.progression.state import (
    ATTRIBUTE_MAX_BY_EVOLUTION,
    ProgressionState,
    SPENDING_COSTS,
)


class EquipmentTests(unittest.TestCase):
    def test_exoskeleton_confirmed_modifiers(self):
        self.assertEqual(EXOSKELETON.strength_bonus, 2)
        self.assertEqual(FULL_EXOSKELETON.strength_bonus, 2)
        self.assertEqual(FULL_EXOSKELETON.reflexes_bonus, 2)

    def test_weapon_can_leave_unresolved_values_empty(self):
        weapon = WeaponDefinition(id="test-weapon", name="Test", damage=None, speed=None)
        self.assertEqual(weapon.category, EquipmentCategory.WEAPON)
        self.assertIsNone(weapon.damage)

    def test_inventory_starts_light(self):
        self.assertEqual(InventoryState().load_category, LoadCategory.LIGHT)


class ProgressionTests(unittest.TestCase):
    def test_confirmed_spending_costs(self):
        self.assertEqual(SPENDING_COSTS["attribute_point"], 1)
        self.assertEqual(SPENDING_COSTS["new_talent"], 3)
        self.assertEqual(SPENDING_COSTS["new_mutation_or_magic"], 4)
        self.assertEqual(SPENDING_COSTS["evolve_mutation_or_magic"], 2)

    def test_points_can_accumulate_and_be_spent(self):
        state = ProgressionState()
        state.add_evolution_points(5)
        self.assertEqual(state.experience_points, 5)
        self.assertEqual(state.spendable_evolution_points, 5)
        self.assertEqual(state.spend("new_talent"), 3)
        self.assertEqual(state.spendable_evolution_points, 2)

    def test_attribute_evolution_limit_is_recorded(self):
        self.assertEqual(ATTRIBUTE_MAX_BY_EVOLUTION, 20)


if __name__ == "__main__":
    unittest.main()
