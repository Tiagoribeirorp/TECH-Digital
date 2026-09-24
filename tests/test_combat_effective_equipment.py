from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.engine import start_combat
from engine.rpg.equipment.definitions import FULL_EXOSKELETON
from engine.rpg.equipment.resolver import equipment_modifier_sources


def character():
    return CharacterState(
        id="hero",
        name="Hero",
        race_id="human",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )


def test_combatant_uses_effective_speed_from_equipment():
    hero = character()
    sources = equipment_modifier_sources({"armor": FULL_EXOSKELETON})
    combat = start_combat([hero, CharacterState(
        id="enemy",
        name="Enemy",
        race_id="human",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )])

    combat.participants[0].modifier_sources = sources
    combat.participants[0].available_speed = combat.participants[0].effective_stats().speed_per_turn

    assert combat.participants[0].available_speed == 6
    assert hero.attributes.reflexes == 10
