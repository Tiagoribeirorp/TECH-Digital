from engine.rpg.combat.damage import apply_damage


def test_damage_reduces_hp_without_going_below_zero():
    result = apply_damage(10, 4)

    assert result.applied_damage == 4
    assert result.remaining_hp == 6
    assert result.became_unconscious is False


def test_damage_at_or_above_hp_causes_unconscious_state():
    result = apply_damage(10, 15)

    assert result.applied_damage == 10
    assert result.remaining_hp == 0
    assert result.became_unconscious is True


def test_negative_damage_is_rejected():
    try:
        apply_damage(10, -1)
    except ValueError:
        pass
    else:
        raise AssertionError("Negative damage should fail")
