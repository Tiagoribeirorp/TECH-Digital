import unittest

from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.engine import (
    begin_execution,
    declaration_order,
    declare_action,
    execution_order,
    finish_round,
    resolve_basic_attack,
    roll_initiative,
    start_combat,
)
from engine.rpg.combat.state import CombatPhase


def make_character(character_id: str, perception: int) -> CharacterState:
    return CharacterState(
        id=character_id,
        name=character_id,
        race_id="test",
        attributes=Attributes(
            strength=10,
            reflexes=10,
            health=10,
            perception=perception,
            intelligence=10,
            willpower=10,
            charisma=10,
        ),
    )


class CombatFlowTests(unittest.TestCase):
    def test_initiative_is_reaction_time_plus_d20(self):
        fast = make_character("fast", 15)
        slow = make_character("slow", 10)
        combat = start_combat([fast, slow])

        rolls = iter([5, 12])
        order = roll_initiative(combat, lambda: next(rolls))

        # fast = 15 + 5 = 20; slow = 10 + 12 = 22
        self.assertEqual(order, ["slow", "fast"])
        self.assertEqual(combat.phase, CombatPhase.DECLARATION)

    def test_declaration_is_slowest_first_and_execution_is_fastest_first(self):
        first = make_character("first", 10)
        second = make_character("second", 14)
        combat = start_combat([first, second])
        roll_initiative(combat, iter([10, 10]).__next__)

        self.assertEqual(execution_order(combat), ["second", "first"])
        self.assertEqual(declaration_order(combat), ["first", "second"])

        declare_action(combat, "first", "attack")
        declare_action(combat, "second", "defend")
        self.assertEqual(combat.get_combatant("first").declared_action, "attack")

    def test_basic_attack_applies_supplied_damage_without_defining_formula(self):
        attacker = make_character("attacker", 12)
        target = make_character("target", 10)
        combat = start_combat([attacker, target])
        roll_initiative(combat, iter([10, 10]).__next__)
        begin_execution(combat)

        result = resolve_basic_attack(
            combat,
            "attacker",
            "target",
            attack_success=True,
            damage=3,
        )

        self.assertEqual(result["damage"], 3)
        self.assertEqual(combat.get_combatant("target").current_hp, 7)

    def test_zero_hp_marks_combatant_unconscious(self):
        attacker = make_character("attacker", 12)
        target = make_character("target", 10)
        combat = start_combat([attacker, target])
        roll_initiative(combat, iter([10, 10]).__next__)
        begin_execution(combat)

        resolve_basic_attack(
            combat,
            "attacker",
            "target",
            attack_success=True,
            damage=10,
        )
        self.assertEqual(combat.get_combatant("target").status, "unconscious")

    def test_round_finishes_when_only_one_active_combatant_remains(self):
        attacker = make_character("attacker", 12)
        target = make_character("target", 10)
        combat = start_combat([attacker, target])
        roll_initiative(combat, iter([10, 10]).__next__)
        begin_execution(combat)
        resolve_basic_attack(
            combat,
            "attacker",
            "target",
            attack_success=True,
            damage=10,
        )
        finish_round(combat)

        self.assertEqual(combat.status, "finished")
        self.assertEqual(combat.phase, CombatPhase.FINISHED)


if __name__ == "__main__":
    unittest.main()
