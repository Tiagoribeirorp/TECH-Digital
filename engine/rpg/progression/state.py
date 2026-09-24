"""Progression data and spending rules.

The source currently contains two incompatible PE progressions. They are kept
as separate tables until the project resolves which one is authoritative.
"""

from dataclasses import dataclass


ATTRIBUTE_MAX_BY_EVOLUTION = 20

SPENDING_COSTS = {
    "attribute_point": 1,
    "new_talent": 3,
    "new_mutation_or_magic": 4,
    "evolve_mutation_or_magic": 2,
    "skill_point": 1,
    "hp_point": 1,
    "fatigue_point": 1,
}

LEVEL_PE_TABLE = {
    1: 0, 2: 5, 3: 5, 4: 6, 5: 6,
    6: 7, 7: 7, 8: 8, 9: 8, 10: 10,
}

COMBAT_REWARD_TABLE = {
    1: 10, 2: 20, 3: 30, 4: 40, 5: 60,
    6: 80, 7: 100, 8: 140, 9: 180, 10: 240,
}

@dataclass
class ProgressionState:
    level: int = 1
    experience_points: int = 0
    spendable_evolution_points: int = 0

    def add_evolution_points(self, points: int) -> None:
        if points < 0:
            raise ValueError("Evolution points cannot be negative")
        self.experience_points += points
        self.spendable_evolution_points += points

    def spend(self, category: str, quantity: int = 1) -> int:
        if category not in SPENDING_COSTS:
            raise KeyError(f"Unknown progression category: {category}")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        cost = SPENDING_COSTS[category] * quantity
        if cost > self.spendable_evolution_points:
            raise ValueError("Not enough spendable evolution points")
        self.spendable_evolution_points -= cost
        return cost
