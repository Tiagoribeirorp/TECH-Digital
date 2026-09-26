"""Integration bridge between the RPG Engine and external clients."""

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from engine.rpg.character.state import Attributes, CharacterState


def get_initial_character_state() -> dict[str, object]:
    character = CharacterState(
        id="hero",
        name="Herói",
        race_id="human",
        attributes=Attributes(
            strength=12,
            reflexes=12,
            health=12,
            perception=12,
            intelligence=12,
            willpower=12,
            charisma=12,
        ),
    )

    character.initialize_resources()
    stats = character.derive_stats()

    return {
        "id": character.id,
        "name": character.name,
        "race_id": character.race_id,
        "hp": character.current_hp,
        "hp_max": stats.hp_max,
        "fatigue": character.current_fatigue,
        "fatigue_max": stats.fatigue_max,
    }


if __name__ == "__main__":
    print(json.dumps(get_initial_character_state(), ensure_ascii=False))