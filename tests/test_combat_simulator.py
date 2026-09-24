"""Tests for the headless basic combat simulator."""

from engine.rpg.combat.simulator import simulate_basic_fight


def test_basic_fight_can_run_to_completion():
    result = simulate_basic_fight(
        initiative_rolls=[10, 5],
        action_rolls=[5, 15, 5, 15] * 10,
        max_rounds=10,
    )

    assert result.combat_status == "finished"
    assert result.winner_id is not None
    assert result.rounds <= 10
    assert result.resolution_count > 0
    assert sum(result.final_hp.values()) > 0


def test_basic_fight_is_reproducible_with_fixed_rolls():
    kwargs = {
        "initiative_rolls": [10, 5],
        "action_rolls": [5, 15] * 10,
        "max_rounds": 10,
    }
    first = simulate_basic_fight(**kwargs)
    second = simulate_basic_fight(**kwargs)

    assert first.winner_id == second.winner_id
    assert first.rounds == second.rounds
    assert first.final_hp == second.final_hp
    assert first.resolution_count == second.resolution_count
