"""Confirmed combat values from equipped weapons, armor and shields.

This module exposes stored equipment values without inventing unresolved
attack, defense or damage formulas.
"""

from engine.rpg.combat.equipment import EquippedCombatEquipment


def weapon_damage(equipment: EquippedCombatEquipment) -> int | None:
    return None if equipment.weapon is None else equipment.weapon.damage


def weapon_speed(equipment: EquippedCombatEquipment, *, surgical: bool = False) -> float | None:
    if equipment.weapon is None or equipment.weapon.speed is None:
        return None
    return equipment.weapon.speed * (2 if surgical else 1)


def armor_defense_bonus(equipment: EquippedCombatEquipment) -> int | None:
    return None if equipment.armor is None else equipment.armor.defense_bonus


def shield_block_bonus(equipment: EquippedCombatEquipment) -> int:
    return 0 if equipment.shield is None else equipment.shield.block_bonus
