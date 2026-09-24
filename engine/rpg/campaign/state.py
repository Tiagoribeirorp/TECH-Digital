"""Campaign and meta-progression state for T.E.C.H. Digital.

This module stores persistent game state without inventing narrative rules.
It intentionally uses generic containers for systems whose detailed rules
have not yet been finalized in the source material.
"""

from dataclasses import dataclass, field
from typing import Any

from engine.rpg.character.state import CharacterState
from engine.rpg.progression.state import ProgressionState


@dataclass
class CampaignState:
    """Persistent state for one playable campaign."""

    id: str
    character: CharacterState
    progression: ProgressionState = field(default_factory=ProgressionState)
    quests: dict[str, dict[str, Any]] = field(default_factory=dict)
    npc_states: dict[str, dict[str, Any]] = field(default_factory=dict)
    faction_states: dict[str, dict[str, Any]] = field(default_factory=dict)
    location_states: dict[str, dict[str, Any]] = field(default_factory=dict)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    discoveries: list[str] = field(default_factory=list)
    active_consequences: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MetaProgression:
    """Progress shared across campaigns.

    The Final Absolute is represented as an explicit state rather than being
    derived from a simple count of completed races.
    """

    completed_races: list[str] = field(default_factory=list)
    fragments: list[str] = field(default_factory=list)
    major_events_discovered: list[str] = field(default_factory=list)
    lore_discovered: list[str] = field(default_factory=list)
    endings_discovered: list[str] = field(default_factory=list)
    absolute_ending_unlocked: bool = False

    def mark_race_completed(self, race_id: str) -> None:
        if race_id not in self.completed_races:
            self.completed_races.append(race_id)

    def add_fragment(self, fragment_id: str) -> None:
        if fragment_id not in self.fragments:
            self.fragments.append(fragment_id)

    def add_major_event(self, event_id: str) -> None:
        if event_id not in self.major_events_discovered:
            self.major_events_discovered.append(event_id)

    def add_lore(self, lore_id: str) -> None:
        if lore_id not in self.lore_discovered:
            self.lore_discovered.append(lore_id)

    def add_ending(self, ending_id: str) -> None:
        if ending_id not in self.endings_discovered:
            self.endings_discovered.append(ending_id)

    def unlock_absolute_ending(self) -> None:
        self.absolute_ending_unlocked = True
