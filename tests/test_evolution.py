from engine.rpg.character.state import Attribute, Attributes, CharacterState
from engine.rpg.progression.evolution import increase_attribute, increase_fatigue, increase_hp, increase_skill
from engine.rpg.progression.state import ProgressionState


def make_character():
    return CharacterState(
        id="hero", name="Hero", race_id="human",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
        current_hp=10, current_fatigue=10,
        skill_values={"combat": 3},
    )


def test_attribute_evolution_spends_one_pe_per_point():
    character = make_character()
    progression = ProgressionState(experience_points=3, spendable_evolution_points=3)

    increase_attribute(character, progression, Attribute.STRENGTH)

    assert character.attributes.strength == 11
    assert progression.spendable_evolution_points == 2


def test_skill_evolution_spends_one_pe_per_point():
    character = make_character()
    progression = ProgressionState(experience_points=2, spendable_evolution_points=2)

    increase_skill(character, progression, "combat", 2)

    assert character.skill_values["combat"] == 5
    assert progression.spendable_evolution_points == 0


def test_hp_and_fatigue_evolution_raise_current_resource_when_present():
    character = make_character()
    progression = ProgressionState(experience_points=2, spendable_evolution_points=2)

    increase_hp(character, progression)
    increase_fatigue(character, progression)

    assert character.attributes.health == 11
    assert character.current_hp == 11
    assert character.attributes.willpower == 11
    assert character.current_fatigue == 11


def test_attribute_cannot_exceed_evolution_maximum():
    character = make_character()
    character.attributes.strength = 20
    progression = ProgressionState(experience_points=1, spendable_evolution_points=1)

    try:
        increase_attribute(character, progression, Attribute.STRENGTH)
    except ValueError:
        pass
    else:
        raise AssertionError("Attribute maximum should be enforced")
