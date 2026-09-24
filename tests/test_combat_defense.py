from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.defense import DefenseMode, resolve_defense


def character():
    return CharacterState(
        id="target",
        name="Target",
        race_id="human",
        attributes=Attributes(10, 12, 10, 14, 10, 10, 10),
    )


def test_evasion_defense_uses_confirmed_formula():
    result = resolve_defense(character(), DefenseMode.EVASION)

    assert result.value == 6.5


def test_parry_requires_skill_and_uses_half_value():
    result = resolve_defense(character(), DefenseMode.PARRY, parry_skill=8)

    assert result.value == 4


def test_block_requires_shield_skill_and_uses_half_value():
    result = resolve_defense(character(), DefenseMode.BLOCK, shield_skill=10)

    assert result.value == 5


def test_dodge_uses_evasion_value_without_inventing_extra_bonus():
    result = resolve_defense(character(), DefenseMode.DODGE)

    assert result.value == 6.5
