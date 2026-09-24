from engine.rpg.combat.actions import CombatAction
from engine.rpg.combat.opposed_attack_action import resolve_opposed_attack_action
from engine.rpg.combat.state import CombatPhase, CombatState, CombatantState
from engine.rpg.character.state import CharacterState, Attributes


def _combat():
    a=CharacterState(id="a", name="A", race_id="human", attributes=Attributes(10,10,10,10,10,10,10))
    b=CharacterState(id="b", name="B", race_id="human", attributes=Attributes(10,10,10,10,10,10,10))
    combat=CombatState(
        participants=[CombatantState.from_character(a), CombatantState.from_character(b)],
        phase=CombatPhase.EXECUTION,
        round_number=1,
        status="active",
    )
    return combat


def test_opposed_attack_applies_damage_and_logs_resolution():
    combat=_combat()
    result=resolve_opposed_attack_action(
        combat,"a","b",
        attack_roll=8, attack_value=13,
        defense_roll=12, defense_value=15,
        damage=4,
    )
    assert result.resolution.attacker_wins is True
    assert result.damage_applied == 4
    assert result.target_hp == 6
    assert len(combat.combat_log) == 1
    assert len(combat.resolution_log) == 1
    assert combat.resolution_log[0].consequences["defense_roll"] == 12


def test_surgical_attack_uses_confirmed_modifiers():
    combat=_combat()
    result=resolve_opposed_attack_action(
        combat,"a","b",
        attack_roll=10, attack_value=10,
        defense_roll=10, defense_value=12,
        damage=4,
        action=CombatAction.SURGICAL_ATTACK,
    )
    assert result.resolution.attacker_wins is True
    assert result.damage_applied == 7


def test_defender_margin_prevents_damage():
    combat=_combat()
    result=resolve_opposed_attack_action(
        combat,"a","b",
        attack_roll=15, attack_value=13,
        defense_roll=5, defense_value=15,
        damage=4,
    )
    assert result.resolution.attacker_wins is False
    assert result.damage_applied == 0
    assert result.target_hp == 10
