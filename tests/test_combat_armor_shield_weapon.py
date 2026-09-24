from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.actions import CombatAction, action_speed_cost
from engine.rpg.combat.defense import DefenseMode, resolve_defense
from engine.rpg.combat.engine import can_execute_action, start_combat
from engine.rpg.equipment.definitions import (
    ArmorDefinition,
    EquipmentInstance,
    ShieldDefinition,
    WeaponDefinition,
)


def character():
    hero = CharacterState(
        id="hero",
        name="Hero",
        race_id="human",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )
    hero.add_item(EquipmentInstance(definition_id="sword", instance_id="sword-1"))
    hero.add_item(EquipmentInstance(definition_id="shield", instance_id="shield-1"))
    hero.add_item(EquipmentInstance(definition_id="armor", instance_id="armor-1"))
    hero.equip_item("sword-1", "weapon")
    hero.equip_item("shield-1", "shield")
    hero.equip_item("armor-1", "armor")
    return hero


def definitions():
    return {
        "sword": WeaponDefinition(id="sword", name="Sword", damage=5, speed=4),
        "shield": ShieldDefinition(id="shield", name="Shield", block_bonus=1, durability=10),
        "armor": ArmorDefinition(id="armor", name="Armor", defense_bonus=2, durability=20),
    }


def test_parry_cost_uses_weapon_speed():
    assert action_speed_cost(CombatAction.PARRY, weapon_speed=4) == 4


def test_parry_can_use_equipped_weapon_speed_in_combat():
    hero = character()
    enemy = CharacterState(
        id="enemy",
        name="Enemy",
        race_id="human",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )
    combat = start_combat([hero, enemy], equipment_definitions=definitions())
    assert can_execute_action(combat, "hero", CombatAction.PARRY) is True


def test_block_includes_confirmed_shield_bonus():
    hero = character()
    combat = start_combat(
        [hero, CharacterState(
            id="enemy",
            name="Enemy",
            race_id="human",
            attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
        )],
        equipment_definitions=definitions(),
    )
    combatant = combat.get_combatant("hero")
    result = resolve_defense(
        hero,
        DefenseMode.BLOCK,
        shield_skill=10,
        equipment=combatant.equipped_combat_equipment,
    )
    assert result.value == 6


def test_armor_defense_is_exposed_without_inventing_attack_formula():
    hero = character()
    combat = start_combat(
        [hero, CharacterState(
            id="enemy",
            name="Enemy",
            race_id="human",
            attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
        )],
        equipment_definitions=definitions(),
    )
    assert combat.get_combatant("hero").equipped_combat_equipment.armor.defense_bonus == 2
