from engine.rpg.core.test_resolution import resolve_d20_test


def test_resolve_d20_test_uses_engine_roller():
    result = resolve_d20_test(12, roller=lambda low, high: 8)
    assert result.roll == 8
    assert result.effective_value == 12
    assert result.success is True
    assert result.margin == 4


def test_resolve_d20_test_preserves_critical_flags():
    critical_success = resolve_d20_test(2, roller=lambda low, high: 1)
    critical_failure = resolve_d20_test(20, roller=lambda low, high: 20)

    assert critical_success.critical_success is True
    assert critical_success.success is True
    assert critical_failure.critical_failure is True
    assert critical_failure.success is False
