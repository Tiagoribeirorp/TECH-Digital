"""Small starter catalog for headless combat prototypes.

All numeric weapon values in this file are provisional until validated by the
author. They exist so the engine can run basic fights without inventing values
inside the combat logic.
"""

from engine.rpg.equipment.definitions import ArmorDefinition, ShieldDefinition, WeaponDefinition


TRAINING_WEAPON = WeaponDefinition(
    id="training_weapon",
    name="Arma de Treino",
    damage=5,
    speed=3,
    range_m=1.5,
    notes="PROVISÓRIO: valores de protótipo.",
)

BASIC_ARMOR = ArmorDefinition(
    id="basic_armor",
    name="Armadura Básica",
    defense_bonus=0,
    durability=10,
    notes="PROVISÓRIO: valores de protótipo.",
)

BASIC_SHIELD = ShieldDefinition(
    id="basic_shield",
    name="Escudo Básico",
    block_bonus=0,
    durability=10,
    notes="PROVISÓRIO: valores de protótipo.",
)

STARTER_EQUIPMENT = {
    TRAINING_WEAPON.id: TRAINING_WEAPON,
    BASIC_ARMOR.id: BASIC_ARMOR,
    BASIC_SHIELD.id: BASIC_SHIELD,
}
