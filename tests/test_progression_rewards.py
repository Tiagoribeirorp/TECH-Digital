from engine.rpg.progression.rewards import apply_reward, resolve_combat_reward
from engine.rpg.progression.state import ProgressionState


def test_combat_reward_uses_explicit_challenge_level():
    reward = resolve_combat_reward(challenge_level=5)
    assert reward.evolution_points == 60
    assert reward.challenge_level == 5


def test_combat_reward_can_use_explicit_points():
    reward = resolve_combat_reward(evolution_points=17)
    assert reward.evolution_points == 17
    assert reward.challenge_level is None


def test_reward_application_updates_progression():
    progression = ProgressionState()
    reward = resolve_combat_reward(challenge_level=2)

    apply_reward(progression, reward)

    assert progression.experience_points == 20
    assert progression.spendable_evolution_points == 20


def test_reward_resolution_does_not_guess_missing_challenge_level():
    try:
        resolve_combat_reward()
    except ValueError as exc:
        assert "challenge level or explicit evolution point amount" in str(exc)
    else:
        raise AssertionError("Missing reward input should fail explicitly")
