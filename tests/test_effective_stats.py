from engine.rpg.character.effective import derive_effective_stats
from engine.rpg.character.state import Attribute, Attributes, CharacterState
from engine.rpg.equipment.definitions import FULL_EXOSKELETON
from engine.rpg.equipment.resolver import equipment_modifier_sources


def make_character():
    return CharacterState(
        id="hero",
        name="Hero",
        race_id="human",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )


def test_exoskeleton_changes_effective_speed_without_mutating_base():
    character = make_character()
    sources = equipment_modifier_sources({"armor": FULL_EXOSKELETON})

    stats = derive_effective_stats(character, *sources)

    assert character.attributes.reflexes == 10
    assert stats.speed_per_turn == 6
    assert stats.evasion == 3


def test_effective_reflexes_are_available_separately():
    character = make_character()
    sources = equipment_modifier_sources({"armor": FULL_EXOSKELETON})

    from engine.rpg.character.effective import effective_attributes_for_character
    effective = effective_attributes_for_character(character, *sources)

    assert effective.get(Attribute.REFLEXES) == 12
    assert effective.get(Attribute.STRENGTH) == 12
