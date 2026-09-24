"""Generic d20 resolution used by the T.E.C.H. Digital prototype."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TestResult:
    roll: int
    target: int
    success: bool
    margin: int

    @property
    def critical_success(self) -> bool:
        return self.roll == 1

    @property
    def critical_failure(self) -> bool:
        return self.roll == 20


def resolve_test(roll: int, effective_value: int) -> TestResult:
    if not 1 <= roll <= 20:
        raise ValueError("d20 roll must be between 1 and 20")

    return TestResult(
        roll=roll,
        target=effective_value,
        success=roll <= effective_value,
        margin=effective_value - roll,
    )


def resolve_resisted_test(first: TestResult, second: TestResult) -> int:
    """Return 1 if first wins, -1 if second wins, 0 if tied."""
    if first.margin > second.margin:
        return 1
    if second.margin > first.margin:
        return -1
    return 0
