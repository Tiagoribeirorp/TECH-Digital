"""Authoritative dice rolling for the T.E.C.H. Digital RPG Engine.

The Presentation Engine may display/animate the returned roll, but it must not
generate a second random result for the same resolution.
"""

from collections.abc import Callable
import random


D20_SIDES = 20
DiceRoller = Callable[[int], int]


def roll_d20(roller: DiceRoller | None = None) -> int:
    """Roll one d20 and return its authoritative result."""
    roll_fn = random.randint if roller is None else roller
    result = roll_fn(1, D20_SIDES)
    if not 1 <= result <= D20_SIDES:
        raise ValueError("d20 roller must return a value between 1 and 20")
    return result
