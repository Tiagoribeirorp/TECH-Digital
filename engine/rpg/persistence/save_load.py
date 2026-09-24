"""Versioned JSON save/load for headless campaign state."""

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from engine.rpg.character.state import CharacterState
from engine.rpg.progression.state import ProgressionState


def character_to_dict(character: CharacterState) -> dict[str, Any]:
    return asdict(character)


def character_from_dict(data: dict[str, Any]) -> CharacterState:
    from engine.rpg.character.state import Attributes
    return CharacterState(
        id=data["id"], name=data["name"], race_id=data["race_id"],
        attributes=Attributes(**data["attributes"]),
        current_hp=data.get("current_hp"),
        current_fatigue=data.get("current_fatigue"),
        skill_values=dict(data.get("skill_values", {})),
        talents=list(data.get("talents", [])),
    )


def save_campaign(path: str | Path, character: CharacterState,
                  progression: ProgressionState | None = None,
                  *, version: int = 1) -> None:
    payload = {
        "save_version": version,
        "character": character_to_dict(character),
        "progression": None if progression is None else asdict(progression),
    }
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_campaign(path: str | Path) -> tuple[CharacterState, ProgressionState | None]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("save_version") != 1:
        raise ValueError("Unsupported save version")
    character = character_from_dict(payload["character"])
    progression_data = payload.get("progression")
    progression = None if progression_data is None else ProgressionState(**progression_data)
    return character, progression
