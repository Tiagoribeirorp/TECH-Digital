"""Headless combat simulator for T.E.C.H. Digital development.

This is a deterministic-friendly prototype harness. It uses provisional combat
values and the engine's real combat resolution, logs and state transitions.
It is not a final gameplay rule set.
"""

from dataclasses import dataclass

from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.engine import (
    begin_execution,
    finish_round,
    roll_initiative,
    start_combat,
)
from engine.rpg.combat.opposed_attack_action import perform_basic_attack
from engine.rpg.equipment.definitions import EquipmentInstance
from engine.rpg.equipment.starter import STARTER_EQUIPMENT


@dataclass(frozen=True)
class SimulationResult:
    winner_id: str | None
    rounds: int
    combat_status: str
    combat_log: list[dict[str, object]]
    resolution_count: int
    final_hp: dict[str, int]


def _character(character_id: str, name: str) -> CharacterState:
    character = CharacterState(
        id=character_id,
        name=name,
        race_id="prototype",
        attributes=Attributes(
            strength=10,
            reflexes=10,
            health=20,
            perception=10,
            intelligence=10,
            willpower=10,
            charisma=10,
        ),
    )
    character.add_item(
        EquipmentInstance(
            definition_id="training_weapon",
            instance_id=f"{character_id}-weapon",
        )
    )
    character.equip_item(f"{character_id}-weapon", "weapon")
    return character


def simulate_basic_fight(
    *,
    initiative_rolls: list[int] | None = None,
    action_rolls: list[int] | None = None,
    max_rounds: int = 20,
) -> SimulationResult:
    """Run a complete two-character fight without Godot.

    Rolls can be supplied to make the simulation reproducible. The action roll
    sequence is consumed as attack/defense pairs.
    """
    hero = _character("hero", "Herói")
    enemy = _character("enemy", "Inimigo")
    combat = start_combat([hero, enemy], equipment_definitions=STARTER_EQUIPMENT)

    initiative_values = initiative_rolls or [10, 10]
    initiative_index = 0

    def initiative_roller() -> int:
        nonlocal initiative_index
        value = initiative_values[initiative_index % len(initiative_values)]
        initiative_index += 1
        return value

    roll_initiative(combat, initiative_roller)

    rolls = action_rolls or [8, 12] * max_rounds
    roll_index = 0

    def action_roller() -> int:
        nonlocal roll_index
        value = rolls[roll_index % len(rolls)]
        roll_index += 1
        return value

    while combat.status == "active" and combat.round_number <= max_rounds:
        begin_execution(combat)

        active = [item for item in combat.participants if item.is_active]
        if len(active) <= 1:
            break

        first, second = active[0], active[1]

        perform_basic_attack(
            combat,
            first.character.id,
            second.character.id,
            roller=action_roller,
        )

        if second.is_active:
            perform_basic_attack(
                combat,
                second.character.id,
                first.character.id,
                roller=action_roller,
            )

        if combat.status == "active":
            finish_round(combat)

    active = [item for item in combat.participants if item.is_active]
    winner_id = active[0].character.id if len(active) == 1 else None

    return SimulationResult(
        winner_id=winner_id,
        rounds=combat.round_number,
        combat_status=combat.status,
        combat_log=list(combat.combat_log),
        resolution_count=len(combat.resolution_log),
        final_hp={
            item.character.id: item.current_hp
            for item in combat.participants
        },
    )


if __name__ == "__main__":
    result = simulate_basic_fight()
    print("=== T.E.C.H. Digital — Basic Combat Simulation ===")
    print(f"Status: {result.combat_status}")
    print(f"Rounds: {result.rounds}")
    print(f"Winner: {result.winner_id}")
    print(f"Final HP: {result.final_hp}")
    print(f"Resolutions: {result.resolution_count}")
