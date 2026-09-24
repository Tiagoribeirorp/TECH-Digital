"""Core character evolution spending."""

from engine.rpg.character.state import Attribute, CharacterState
from engine.rpg.progression.state import ATTRIBUTE_MAX_BY_EVOLUTION, ProgressionState


def increase_attribute(character, progression, attribute, quantity=1):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    current = character.attributes.get(attribute)
    if current + quantity > ATTRIBUTE_MAX_BY_EVOLUTION:
        raise ValueError("Attribute would exceed the evolution maximum")
    cost = progression.spend("attribute_point", quantity)
    setattr(character.attributes, attribute.value, current + quantity)
    return cost


def increase_skill(character, progression, skill, quantity=1):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if skill not in character.skill_values:
        raise KeyError(f"Unknown skill: {skill}")
    cost = progression.spend("skill_point", quantity)
    character.skill_values[skill] += quantity
    return cost


def increase_hp(character, progression, quantity=1):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    cost = progression.spend("hp_point", quantity)
    character.attributes.health += quantity
    if character.current_hp is not None:
        character.current_hp += quantity
    return cost


def increase_fatigue(character, progression, quantity=1):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    cost = progression.spend("fatigue_point", quantity)
    character.attributes.willpower += quantity
    if character.current_fatigue is not None:
        character.current_fatigue += quantity
    return cost
