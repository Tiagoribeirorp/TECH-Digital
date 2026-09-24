from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.engine import begin_execution, resolve_basic_attack, roll_initiative, start_combat


def make_character(character_id: str) -> CharacterState:
    return CharacterState(
        id=character_id,
        name=character_id,
        race_id="test",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )


def test_attack_creates_structured_resolution_record():
    combat = start_combat([make_character("a"), make_character("b")])
    roll_initiative(combat, iter([10, 10]).__next__)
    begin_execution(combat)

    result = resolve_basic_attack(
        combat,
        "a",
        "b",
        attack_success=True,
        damage=3,
        random_roll=7,
        modifiers={"attack": 2},
        effective_value=12,
    )

    assert result["resolution_sequence"] == 1
    assert len(combat.resolution_log) == 1
    record = combat.resolution_log[0]
    assert record.action == "attack"
    assert record.random_roll == 7
    assert record.modifiers == {"attack": 2}
    assert record.effective_value == 12
    assert record.consequences["damage"] == 3
    assert record.consequences["target_hp"] == 7
