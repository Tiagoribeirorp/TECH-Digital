"""Versioned JSON save/load for the headless character/progression prototype."""

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.equipment.definitions import EquipmentInstance, InventoryState, LoadCategory
from engine.rpg.progression.state import ProgressionState


def character_to_dict(character: CharacterState) -> dict[str, Any]:
    return asdict(character)


def character_from_dict(data: dict[str, Any]) -> CharacterState:
    inventory_data = data.get("inventory", {})
    inventory = InventoryState(
        items=[
            EquipmentInstance(
                definition_id=item["definition_id"],
                instance_id=item["instance_id"],
                durability_current=item.get("durability_current"),
                equipped=bool(item.get("equipped", False)),
            )
            for item in inventory_data.get("items", [])
        ],
        load_category=LoadCategory(
            inventory_data.get("load_category", LoadCategory.LIGHT.value)
        ),
    )
    return CharacterState(
        id=data["id"],
        name=data["name"],
        race_id=data["race_id"],
        attributes=Attributes(**data["attributes"]),
        current_hp=data.get("current_hp"),
        current_fatigue=data.get("current_fatigue"),
        skill_values=dict(data.get("skill_values", {})),
        talents=list(data.get("talents", [])),
        inventory=inventory,
        equipped=dict(data.get("equipped", {})),
    )


def save_campaign(
    path: str | Path,
    character: CharacterState,
    progression: ProgressionState | None = None,
    *,
    version: int = 1,
) -> None:
    payload = {
        "save_version": version,
        "character": character_to_dict(character),
        "progression": None if progression is None else asdict(progression),
    }
    Path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_campaign(
    path: str | Path,
) -> tuple[CharacterState, ProgressionState | None]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("save_version") != 1:
        raise ValueError("Unsupported save version")
    character = character_from_dict(payload["character"])
    progression_data = payload.get("progression")
    progression = (
        None
        if progression_data is None
        else ProgressionState(**progression_data)
    )
    return character, progression
