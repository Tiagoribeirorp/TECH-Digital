from engine.rpg.combat.opposed_attack import resolve_opposed_attack


def test_opposed_attack_uses_margin_and_only_attacker_higher_wins():
    result = resolve_opposed_attack(
        attack_roll=8,
        attack_value=13,
        defense_roll=12,
        defense_value=15,
        damage=6,
    )
    assert result.attack.margin == 5
    assert result.defense.margin == 3
    assert result.attacker_wins is True
    assert result.margin_difference == 2
    assert result.damage_applies is True


def test_defense_with_higher_margin_prevents_damage():
    result = resolve_opposed_attack(
        attack_roll=10,
        attack_value=12,
        defense_roll=5,
        defense_value=15,
        damage=6,
    )
    assert result.attacker_wins is False
    assert result.damage_applies is False


def test_tied_margin_does_not_apply_attack_damage():
    result = resolve_opposed_attack(
        attack_roll=8,
        attack_value=13,
        defense_roll=10,
        defense_value=15,
        damage=6,
    )
    assert result.margin_difference == 0
    assert result.attacker_wins is False
    assert result.damage_applies is False
