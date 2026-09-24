"""Core character state for the T.E.C.H. Digital RPG Engine prototype."""

from dataclasses import dataclass, field
from enum import Enum

from engine.rpg.equipment.definitions import EquipmentInstance, InventoryState


class Attribute(str, Enum):
    STRENGTH = "strength"
    REFLEXES = "reflexes"
    HEALTH = "health"
    PERCEPTION = "perception"
    INTELLIGENCE = "intelligence"
    WILLPOWER = "willpower"
    CHARISMA = "charisma"


@dataclass
class Attributes:
    strength: int
    reflexes: int
    health: int
    perception: int
    intelligence: int
    willpower: int
    charisma: int

    def get(self, attribute: Attribute) -> int:
        return getattr(self, attribute.value)

    def as_dict(self) -> dict[str, int]:
        return {
            "strength": self.strength,
            "reflexes": self.reflexes,
            "health": self.health,
            "perception": self.perception,
            "intelligence": self.intelligence,
            "willpower": self.willpower,
            "charisma": self.charisma,
        }


@dataclass
class DerivedStats:
    reaction: int
    evasion: float
    parry: float | None
    block: float | None
    senses: int
    reaction_time_base: int
    speed_per_turn: float
    movement_per_speed: float
    hp_max: int
    fatigue_max: int


@dataclass
class CharacterState:
    id: str
    name: str
    race_id: str
    attributes: Attributes
    current_hp: int | None = None
    current_fatigue: int | None = None
    skill_values: dict[str, int] = field(default_factory=dict)
    talents: list[str] = field(default_factory=list)
    inventory: InventoryState = field(default_factory=InventoryState)
    equipped: dict[str, str] = field(default_factory=dict)

    def derive_stats(
        self,
        *,
        parry_skill: int | None = None,
        shield_skill: int | None = None,
    ) -> DerivedStats:
        """Calculate confirmed derived values from the project specification.

        Evasion and Speed per Turn intentionally remain fractional here.
        The source documents identify rounding as a validation item.
        """
        return DerivedStats(
            reaction=self.attributes.charisma,
            evasion=(self.attributes.reflexes + self.attributes.perception) / 4,
            parry=None if parry_skill is None else parry_skill / 2,
            block=None if shield_skill is None else shield_skill / 2,
            senses=self.attributes.perception,
            reaction_time_base=self.attributes.perception,
            speed_per_turn=self.attributes.reflexes / 2,
            movement_per_speed=1.5,
            hp_max=self.attributes.health,
            fatigue_max=self.attributes.willpower,
        )

    def initialize_resources(self) -> None:
        stats = self.derive_stats()
        if self.current_hp is None:
            self.current_hp = stats.hp_max
        if self.current_fatigue is None:
            self.current_fatigue = stats.fatigue_max

    def effective_skill(self, skill: str, modifier: int = 0) -> int:
        if skill not in self.skill_values:
            raise KeyError(f"Unknown skill: {skill}")
        return self.skill_values[skill] + modifier

    def add_item(self, item: EquipmentInstance) -> None:
        self.inventory.items.append(item)

    def equip_item(self, instance_id: str, slot: str) -> None:
        item = next(
            (item for item in self.inventory.items if item.instance_id == instance_id),
            None,
        )
        if item is None:
            raise KeyError(f"Unknown equipment instance: {instance_id}")

        previous_id = self.equipped.get(slot)
        if previous_id is not None:
            self._set_equipped_flag(previous_id, False)

        self.equipped[slot] = instance_id
        item.equipped = True

    def unequip_slot(self, slot: str) -> None:
        instance_id = self.equipped.pop(slot, None)
        if instance_id is not None:
            self._set_equipped_flag(instance_id, False)

    def get_equipped(self, slot: str) -> EquipmentInstance | None:
        instance_id = self.equipped.get(slot)
        if instance_id is None:
            return None
        return next(
            (item for item in self.inventory.items if item.instance_id == instance_id),
            None,
        )

    def _set_equipped_flag(self, instance_id: str, equipped: bool) -> None:
        item = next(
            (item for item in self.inventory.items if item.instance_id == instance_id),
            None,
        )
        if item is not None:
            item.equipped = equipped
