import tempfile
import unittest
from pathlib import Path

from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.persistence.save_load import load_campaign, save_campaign
from engine.rpg.progression.state import ProgressionState


class SaveLoadTests(unittest.TestCase):
    def test_campaign_round_trip(self):
        character = CharacterState(
            id="hero", name="Heroi", race_id="human",
            attributes=Attributes(10,11,12,13,14,15,16),
            current_hp=9, current_fatigue=12,
            skill_values={"furtividade": 13},
            talents=["talent-test"],
        )
        progression = ProgressionState(level=2, experience_points=5, spendable_evolution_points=2)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "save.json"
            save_campaign(path, character, progression)
            loaded_character, loaded_progression = load_campaign(path)
        self.assertEqual(loaded_character.name, "Heroi")
        self.assertEqual(loaded_character.attributes.perception, 13)
        self.assertEqual(loaded_progression.spendable_evolution_points, 2)


if __name__ == "__main__":
    unittest.main()
