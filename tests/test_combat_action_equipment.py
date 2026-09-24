from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.resolution import resolve_attack_action
from engine.rpg.combat.state import CombatantState
from engine.rpg.combat.actions import CombatAction
from engine.rpg.equipment.definitions import WeaponDefinition, EquipmentInstance


def hero_with_weapon():
    hero = CharacterState(
        id="hero",
        name="Hero",
        race_id="human",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )
    hero.add_item(EquipmentInstance(definition_id="sword", instance_id="sword-1"))
    hero.equip_item("sword-1", "weapon")
    combatant = CombatantState.from_character(
        hero,
        equipment_definitions={
            "sword": WeaponDefinition(
                id="sword",
                name="Sword",
                damage=5,
                speed=4,
            )
        },
    )
    return combatant


def test_surgical_attack_applies_confirmed_attack_and_damage_modifiers():
    combatant = hero_with_weapon()

    result = resolve_attack_action(
        action=CombatAction.SURGICAL_ATTACK,
        roll=10,
        attack_value=10,
        combatant=combatant,
    )

    assert result.attack.effective_attack_value == 13
    assert result.final_damage == 8
    assert result.weapon_speed == 8


def test_fight_defensively_applies_negative_attack_modifier():
    combatant = hero_with_weapon()

    result = resolve_attack_action(
        action=CombatAction.FIGHT_DEFENSIVELY,
        roll=10,
        attack_value=10,
        combatant=combatant,
    )

    assert result.attack.effective_attack_value == 7
    assert result.final_damage == 5


def test_explicit_damage_overrides_weapon_damage():
    combatant = hero_with_weapon()

    result = resolve_attack_action(
        action=CombatAction.ATTACK,
        roll=10,
        attack_value=10,
        combatant=combatant,
        base_damage=9,
    )

    assert result.final_damage == 9
