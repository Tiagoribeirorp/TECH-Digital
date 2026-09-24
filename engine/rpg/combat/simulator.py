"""Headless combat simulator for attack announcements and reactions.

This prototype models: declaration -> attack announcement -> defender reaction
-> execution -> opposed attack resolution. Final attack/defense formulas remain
configurable because some source rules are still pending validation.
"""

from dataclasses import dataclass

from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.actions import CombatAction
from engine.rpg.combat.basic_actions import select_defense_choice
from engine.rpg.combat.engine import begin_execution, declare_action, finish_round, roll_initiative, start_combat
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


def simulate_reactive_fight(
    *,
    initiative_rolls: list[int] | None = None,
    action_rolls: list[int] | None = None,
    max_rounds: int = 20,
    defender_reaction: CombatAction = CombatAction.DODGE,
) -> SimulationResult:
    """Run a deterministic two-character fight with a defense reaction window."""
    if defender_reaction not in {
        CombatAction.DODGE,
        CombatAction.PARRY,
        CombatAction.BLOCK,
    }:
        raise ValueError("defender_reaction must be DODGE, PARRY or BLOCK")

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
        # Announcement phase: the slower side declares first.
        for character_id in reversed(combat.initiative_order):
            combatant = combat.get_combatant(character_id)
            if combatant.is_active:
                declare_action(combat, character_id, CombatAction.ATTACK.value)

        attacker_id, target_id = combat.initiative_order[:2]
        combat.combat_log.append({
            "event": "attack_announced",
            "round": combat.round_number,
            "attacker_id": attacker_id,
            "target_id": target_id,
        })

        # Reaction window: the target chooses its defense after the attack is announced.
        target = combat.get_combatant(target_id)
        if target.is_active:
            weapon = target.equipped_combat_equipment.weapon
            select_defense_choice(
                combat,
                target_id,
                defender_reaction,
                weapon_speed=None if weapon is None else weapon.speed,
            )

        begin_execution(combat)

        if (
            combat.get_combatant(attacker_id).is_active
            and combat.get_combatant(target_id).is_active
        ):
            perform_basic_attack(
                combat,
                attacker_id,
                target_id,
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


def simulate_basic_fight(**kwargs) -> SimulationResult:
    """Backward-compatible alias for the original simulator entry point."""
    return simulate_reactive_fight(**kwargs)


if __name__ == "__main__":
    result = simulate_reactive_fight()
    print("=== T.E.C.H. Digital — Reactive Combat Simulation ===")
    print(f"Status: {result.combat_status}")
    print(f"Rounds: {result.rounds}")
    print(f"Winner: {result.winner_id}")
    print(f"Final HP: {result.final_hp}")
    print(f"Resolutions: {result.resolution_count}")
