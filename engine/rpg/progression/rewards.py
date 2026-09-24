"""Reward resolution for progression events.

The source defines a combat/challenge reward table, but it does not define
how a particular combat is classified. Therefore callers must provide the
challenge level explicitly or provide an explicit Evolution Point amount.
"""

from dataclasses import dataclass

from engine.rpg.campaign.state import CampaignState
from engine.rpg.progression.state import COMBAT_REWARD_TABLE, ProgressionState


@dataclass(frozen=True)
class RewardResult:
    """A resolved progression reward before/after application."""

    source: str
    evolution_points: int
    challenge_level: int | None = None


def resolve_combat_reward(*, challenge_level: int | None = None,
                          evolution_points: int | None = None) -> RewardResult:
    """Resolve a combat reward without guessing its challenge level."""
    if challenge_level is not None and evolution_points is not None:
        raise ValueError("Provide challenge_level or evolution_points, not both")

    if challenge_level is not None:
        if challenge_level not in COMBAT_REWARD_TABLE:
            raise ValueError("Challenge level must be between 1 and 10")
        return RewardResult(
            source="combat",
            evolution_points=COMBAT_REWARD_TABLE[challenge_level],
            challenge_level=challenge_level,
        )

    if evolution_points is None:
        raise ValueError("A challenge level or explicit evolution point amount is required")
    if evolution_points < 0:
        raise ValueError("Evolution points cannot be negative")

    return RewardResult(source="combat", evolution_points=evolution_points)


def apply_reward(progression: ProgressionState, reward: RewardResult) -> RewardResult:
    """Apply a previously resolved reward to progression."""
    progression.add_evolution_points(reward.evolution_points)
    return reward


def award_combat_reward(
    campaign: CampaignState,
    *,
    challenge_level: int | None = None,
    evolution_points: int | None = None,
) -> RewardResult:
    """Resolve and apply a combat reward to the active campaign."""
    reward = resolve_combat_reward(
        challenge_level=challenge_level,
        evolution_points=evolution_points,
    )
    apply_reward(campaign.progression, reward)
    campaign.events.append({
        "type": "progression_reward",
        "source": reward.source,
        "evolution_points": reward.evolution_points,
        "challenge_level": reward.challenge_level,
    })
    return reward
