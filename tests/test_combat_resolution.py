from engine.rpg.combat.resolution import resolve_attack_test


def test_attack_resolution_applies_action_modifier():
    result = resolve_attack_test(roll=10, attack_value=10, attack_modifier=3)

    assert result.effective_attack_value == 13
    assert result.test.success is True
    assert result.test.margin == 3


def test_attack_resolution_preserves_critical_results():
    success = resolve_attack_test(roll=1, attack_value=1)
    failure = resolve_attack_test(roll=20, attack_value=20)

    assert success.test.critical_success is True
    assert success.test.success is True
    assert failure.test.critical_failure is True
    assert failure.test.success is False


def test_attack_resolution_rejects_invalid_roll():
    try:
        resolve_attack_test(roll=21, attack_value=10)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid d20 roll should fail")
