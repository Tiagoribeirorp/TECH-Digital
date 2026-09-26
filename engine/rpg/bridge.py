"""Integration bridge between the RPG Engine and external clients."""

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from engine.rpg.character.state import Attributes, CharacterState


def create_character(
    *,
    current_hp: int | None = None,
    current_fatigue: int | None = None,
) -> CharacterState:
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
        current_hp=current_hp,
        current_fatigue=current_fatigue,
    )

    character.initialize_resources()
    return character


def character_state(character: CharacterState) -> dict[str, object]:
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


def execute_action(character: CharacterState) -> None:
    """Temporary gameplay action used to validate the Godot/Engine bridge."""

    fatigue_cost = 2

    character.current_fatigue = max(
        0,
        character.current_fatigue - fatigue_cost,
    )


def get_initial_character_state() -> dict[str, object]:
    character = create_character()
    return character_state(character)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["basic"], default=None)
    parser.add_argument("--hp", type=int, default=None)
    parser.add_argument("--fatigue", type=int, default=None)

    args = parser.parse_args()

    character = create_character(
        current_hp=args.hp,
        current_fatigue=args.fatigue,
    )

    if args.action == "basic":
        execute_action(character)

    print(
        json.dumps(
            character_state(character),
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()