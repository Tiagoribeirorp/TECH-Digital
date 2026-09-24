"""Tests for the authoritative d20 roller."""

import pytest

from engine.rpg.core.dice import roll_d20


def test_roll_d20_uses_supplied_roller():
    assert roll_d20(lambda low, high: 8) == 8


def test_roll_d20_rejects_invalid_supplied_result():
    with pytest.raises(ValueError):
        roll_d20(lambda low, high: 0)


def test_roll_d20_rejects_result_above_d20():
    with pytest.raises(ValueError):
        roll_d20(lambda low, high: 21)
