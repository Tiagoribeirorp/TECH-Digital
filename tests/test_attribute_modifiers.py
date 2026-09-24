from engine.rpg.character.modifiers import (
    ModifierSource,
    effective_attributes,
)
from engine.rpg.character.state import Attribute, Attributes
from engine.rpg.equipment.definitions import EXOSKELETON, FULL_EXOSKELETON
from engine.rpg.equipment.modifiers import attribute_modifier_source


def base_attributes() -> Attributes:
    return Attributes(10, 11, 12, 13, 14, 15, 16)


def test_modifiers_do_not_mutate_base_attributes():
    base = base_attributes()
    effective = effective_attributes(
        base,
        attribute_modifier_source(EXOSKELETON),
    )

    assert base.strength == 10
    assert effective.get(Attribute.STRENGTH) == 12
    assert effective.get(Attribute.REFLEXES) == 11


def test_full_exoskeleton_adds_both_confirmed_modifiers():
    effective = effective_attributes(
        base_attributes(),
        attribute_modifier_source(FULL_EXOSKELETON),
    )

    assert effective.as_dict()["strength"] == 12
    assert effective.as_dict()["reflexes"] == 13


def test_multiple_sources_are_accumulated():
    effective = effective_attributes(
        base_attributes(),
        ModifierSource("race", {"strength": 2}),
        ModifierSource("talent", {"strength": 1, "charisma": -1}),
    )

    assert effective.get(Attribute.STRENGTH) == 13
    assert effective.get(Attribute.CHARISMA) == 15
