"""Authoritative d20 test resolution for T.E.C.H. Digital.

The engine owns the random roll and the mechanical result. Presentation layers
may animate the returned roll, but they do not generate the outcome.
"""

from dataclasses import dataclass

from engine.rpg.core.dice import DiceRoller, roll_d20
from engine.rpg.core.tests import TestResult, resolve_test


@dataclass(frozen=True)
class TestResolution:
    """Complete result of one standard d20 test."""

    test: TestResult
    source: str = ""
    actor_id: str | None = None
    target_id: str | None = None

    @property
    def roll(self) -> int:
        return self.test.roll

    @property
    def effective_value(self) -> int:
        return self.test.target

    @property
    def success(self) -> bool:
        return self.test.success

    @property
    def margin(self) -> int:
        return self.test.margin

    @property
    def critical_success(self) -> bool:
        return self.test.critical_success

    @property
    def critical_failure(self) -> bool:
        return self.test.critical_failure


def resolve_d20_test(
    effective_value: int,
    *,
    roller: DiceRoller | None = None,
    source: str = "",
    actor_id: str | None = None,
    target_id: str | None = None,
) -> TestResolution:
    """Roll and resolve one authoritative d20 test."""
    roll = roll_d20(roller)
    result = resolve_test(roll, effective_value)
    return TestResolution(
        test=result,
        source=source,
        actor_id=actor_id,
        target_id=target_id,
    )
