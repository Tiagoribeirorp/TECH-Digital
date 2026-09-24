from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.equipment.definitions import EquipmentInstance, InventoryState, LoadCategory


def make_character() -> CharacterState:
    return CharacterState(
        id="hero-1",
        name="Hero",
        race_id="human",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )


def test_character_can_add_and_equip_item():
    character = make_character()
    weapon = EquipmentInstance(definition_id="sword", instance_id="sword-1")

    character.add_item(weapon)
    character.equip_item("sword-1", "main_hand")

    assert character.equipped == {"main_hand": "sword-1"}
    assert character.get_equipped("main_hand") is weapon
    assert weapon.equipped is True


def test_equipping_replaces_previous_item_in_same_slot():
    character = make_character()
    first = EquipmentInstance(definition_id="sword", instance_id="sword-1")
    second = EquipmentInstance(definition_id="axe", instance_id="axe-1")

    character.add_item(first)
    character.add_item(second)
    character.equip_item("sword-1", "main_hand")
    character.equip_item("axe-1", "main_hand")

    assert character.get_equipped("main_hand") is second
    assert first.equipped is False
    assert second.equipped is True


def test_unequip_slot_updates_item_state():
    character = make_character()
    shield = EquipmentInstance(definition_id="shield", instance_id="shield-1")

    character.add_item(shield)
    character.equip_item("shield-1", "off_hand")
    character.unequip_slot("off_hand")

    assert character.get_equipped("off_hand") is None
    assert shield.equipped is False


def test_inventory_load_category_is_preserved():
    character = make_character()
    character.inventory = InventoryState(load_category=LoadCategory.MEDIUM)

    assert character.inventory.load_category == LoadCategory.MEDIUM
