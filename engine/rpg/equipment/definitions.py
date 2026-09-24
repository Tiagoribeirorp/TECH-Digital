"""Equipment definitions for the T.E.C.H. Digital RPG Engine.

Only confirmed effects are encoded. Unresolved weapon statistics and load
capacity formulas remain data fields rather than invented rules.
"""

from dataclasses import dataclass, field
from enum import Enum


class EquipmentCategory(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    SHIELD = "shield"
    EXOSKELETON = "exoskeleton"
    ITEM = "item"


class LoadCategory(str, Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"


@dataclass(frozen=True)
class EquipmentDefinition:
    id: str
    name: str
    category: EquipmentCategory
    notes: str = ""


@dataclass(frozen=True)
class WeaponDefinition(EquipmentDefinition):
    category: EquipmentCategory = EquipmentCategory.WEAPON
    damage: int | None = None
    speed: float | None = None
    range_m: float | None = None


@dataclass(frozen=True)
class ArmorDefinition(EquipmentDefinition):
    category: EquipmentCategory = EquipmentCategory.ARMOR
    defense_bonus: int | None = None
    durability: int | None = None


@dataclass(frozen=True)
class ShieldDefinition(EquipmentDefinition):
    category: EquipmentCategory = EquipmentCategory.SHIELD
    block_bonus: int = 0
    durability: int | None = None


@dataclass(frozen=True)
class ExoskeletonDefinition(EquipmentDefinition):
    category: EquipmentCategory = EquipmentCategory.EXOSKELETON
    strength_bonus: int = 0
    reflexes_bonus: int = 0


@dataclass
class EquipmentInstance:
    definition_id: str
    instance_id: str
    durability_current: int | None = None
    equipped: bool = False


@dataclass
class InventoryState:
    items: list[EquipmentInstance] = field(default_factory=list)
    load_category: LoadCategory = LoadCategory.LIGHT


# Confirmed effects from the project material.
EXOSKELETON = ExoskeletonDefinition(
    id="exoskeleton",
    name="Exoesqueleto",
    strength_bonus=2,
)
FULL_EXOSKELETON = ExoskeletonDefinition(
    id="full_exoskeleton",
    name="Exoesqueleto Completo",
    strength_bonus=2,
    reflexes_bonus=2,
)
