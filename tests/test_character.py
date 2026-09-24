import unittest

from engine.rpg.character.definitions import RaceDefinition, resolve_skill_value
from engine.rpg.character.factory import apply_race
from engine.rpg.character.state import Attributes, CharacterState


class RaceTests(unittest.TestCase):
    def test_race_attribute_modifiers_are_applied(self):
        character = CharacterState(
            id="1",
            name="Test",
            race_id="base",
            attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
        )
        orc = RaceDefinition(
            id="orc",
            name="Orc",
            attribute_modifiers={"strength": 2, "health": 2, "charisma": -2},
        )
        result = apply_race(character, orc)
        self.assertEqual(result.race_id, "orc")
        self.assertEqual(result.attributes.strength, 12)
        self.assertEqual(result.attributes.health, 12)
        self.assertEqual(result.attributes.charisma, 8)


class SkillTests(unittest.TestCase):
    def test_documented_skill_investment_table(self):
        attrs = (12,)
        self.assertEqual(resolve_skill_value(points=1, attribute_values=attrs), 10)
        self.assertEqual(resolve_skill_value(points=2, attribute_values=attrs), 11)
        self.assertEqual(resolve_skill_value(points=3, attribute_values=attrs), 12)
        self.assertEqual(resolve_skill_value(points=4, attribute_values=attrs), 13)
        self.assertEqual(resolve_skill_value(points=5, attribute_values=attrs), 14)

    def test_untrained_penalty_is_explicit(self):
        self.assertEqual(
            resolve_skill_value(
                points=0,
                attribute_values=(12,),
                untrained_penalty=-3,
            ),
            9,
        )


if __name__ == "__main__":
    unittest.main()
