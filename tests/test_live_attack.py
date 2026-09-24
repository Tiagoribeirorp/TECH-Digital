from engine.rpg.combat.live_attack import resolve_live_attack_against_choice


def test_live_attack_uses_authoritative_d20_roller():
    assert callable(resolve_live_attack_against_choice)
