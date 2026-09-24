"""Persistence helpers for full campaign and meta-progression state."""

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from engine.rpg.campaign.state import CampaignState, MetaProgression
from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.equipment.definitions import EquipmentInstance, InventoryState, LoadCategory


SAVE_VERSION = 2


def _character_from_dict(data: dict[str, Any]) -> CharacterState:
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


def campaign_to_dict(campaign: CampaignState) -> dict[str, Any]:
    return asdict(campaign)


def campaign_from_dict(data: dict[str, Any]) -> CampaignState:
    return CampaignState(
        id=data["id"],
        character=_character_from_dict(data["character"]),
        quests=dict(data.get("quests", {})),
        npc_states=dict(data.get("npc_states", {})),
        faction_states=dict(data.get("faction_states", {})),
        location_states=dict(data.get("location_states", {})),
        decisions=list(data.get("decisions", [])),
        events=list(data.get("events", [])),
        discoveries=list(data.get("discoveries", [])),
        active_consequences=list(data.get("active_consequences", [])),
    )


def meta_to_dict(meta: MetaProgression) -> dict[str, Any]:
    return asdict(meta)


def meta_from_dict(data: dict[str, Any]) -> MetaProgression:
    return MetaProgression(
        completed_races=list(data.get("completed_races", [])),
        fragments=list(data.get("fragments", [])),
        major_events_discovered=list(data.get("major_events_discovered", [])),
        lore_discovered=list(data.get("lore_discovered", [])),
        endings_discovered=list(data.get("endings_discovered", [])),
        absolute_ending_unlocked=bool(data.get("absolute_ending_unlocked", False)),
    )


def save_full_state(
    path: str | Path,
    campaign: CampaignState,
    meta_progression: MetaProgression,
    *,
    version: int = SAVE_VERSION,
) -> None:
    payload = {
        "save_version": version,
        "campaign": campaign_to_dict(campaign),
        "meta_progression": meta_to_dict(meta_progression),
    }
    Path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_full_state(
    path: str | Path,
) -> tuple[CampaignState, MetaProgression]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("save_version") != SAVE_VERSION:
        raise ValueError("Unsupported save version")

    return (
        campaign_from_dict(payload["campaign"]),
        meta_from_dict(payload["meta_progression"]),
    )
