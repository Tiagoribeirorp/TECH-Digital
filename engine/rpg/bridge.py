"""Integration bridge between the RPG Engine and external clients."""

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.engine import (
    begin_execution,
    resolve_basic_attack,
    roll_initiative,
    start_combat,
)
from engine.rpg.combat.actions import CombatAction
from engine.rpg.combat.resolution import resolve_attack_action
from engine.rpg.combat.state import CombatPhase
from engine.rpg.core.dice import roll_d20


ATTACK_TARGET = 12
ATTACK_DAMAGE = 5
ATTACK_FATIGUE_COST = 2
DEFEND_FATIGUE_COST = 1
SPECIAL_FATIGUE_COST = 3
DEFEND_BONUS = 4
ENEMY_HP = 10
ENEMY_ATTACK_TARGET = 10
ENEMY_ATTACK_DAMAGE = 3
RECOVER_FATIGUE_AMOUNT = 2

ENEMY_PROFILES = {
    "training_dummy": {
        "name": "Alvo de treino",
        "health": 10,
        "attributes": (10, 10, 10, 10, 10, 10, 10),
        "attack_target": 10,
        "attack_damage": 3,
    },
    "raider": {
        "name": "Saqueador",
        "health": 12,
        "attributes": (11, 11, 10, 10, 8, 9, 8),
        "attack_target": 11,
        "attack_damage": 4,
    },
}


def create_character(
    *,
    current_hp: int | None = None,
    current_fatigue: int | None = None,
) -> CharacterState:
    character = CharacterState(
        id="hero",
        name="Herói",
        race_id="human",
        attributes=Attributes(
            strength=12,
            reflexes=12,
            health=12,
            perception=12,
            intelligence=12,
            willpower=12,
            charisma=12,
        ),
        current_hp=current_hp,
        current_fatigue=current_fatigue,
    )

    character.initialize_resources()
    return character


def character_state(character: CharacterState) -> dict[str, object]:
    stats = character.derive_stats()

    return {
        "id": character.id,
        "name": character.name,
        "race_id": character.race_id,
        "hp": character.current_hp,
        "hp_max": stats.hp_max,
        "fatigue": character.current_fatigue,
        "fatigue_max": stats.fatigue_max,
    }


def execute_action(character: CharacterState) -> None:
    """Temporary gameplay action used to validate the Godot/Engine bridge."""

    fatigue_cost = 2

    character.current_fatigue = max(
        0,
        character.current_fatigue - fatigue_cost,
    )


def create_enemy(
    *,
    enemy_type: str = "training_dummy",
    current_hp: int | None = None,
) -> CharacterState:
    if enemy_type not in ENEMY_PROFILES:
        raise ValueError(f"Unknown enemy type: {enemy_type}")
    profile = ENEMY_PROFILES[enemy_type]
    enemy = CharacterState(
        id="training_enemy",
        name=str(profile["name"]),
        race_id=enemy_type,
        attributes=Attributes(*profile["attributes"]),
        current_hp=profile["health"] if current_hp is None else current_hp,
    )
    enemy.initialize_resources()
    return enemy


def roll_combat_initiative(
    *,
    hero_roll: int | None = None,
    enemy_roll: int | None = None,
) -> dict[str, object]:
    """Roll initiative once before combat and return the resulting order."""
    resolved_hero_roll = roll_d20() if hero_roll is None else hero_roll
    resolved_enemy_roll = roll_d20() if enemy_roll is None else enemy_roll
    first = "hero" if resolved_hero_roll >= resolved_enemy_roll else "enemy"
    return {
        "hero_roll": resolved_hero_roll,
        "enemy_roll": resolved_enemy_roll,
        "first": first,
        "order": ["hero", "enemy"] if first == "hero" else ["enemy", "hero"],
    }


def execute_combat_action(
    *,
    action: str,
    current_hp: int,
    current_fatigue: int,
    enemy_hp: int,
    forced_roll: int | None = None,
    round_number: int = 1,
    enemy_type: str = "training_dummy",
) -> dict[str, object]:
    hero = create_character(
        current_hp=current_hp,
        current_fatigue=current_fatigue,
    )
    enemy = create_enemy(enemy_type=enemy_type, current_hp=enemy_hp)
    enemy_profile = ENEMY_PROFILES[enemy_type]
    combat = start_combat([hero, enemy])
    roll_initiative(combat, lambda: 10)
    combat.phase = CombatPhase.DECLARATION
    begin_execution(combat)

    if action not in {CombatAction.ATTACK.value, "defend", "special", "recover"}:
        raise ValueError(f"Unknown combat action: {action}")

    is_defending = action == "defend"
    is_recovering = action == "recover"
    fatigue_cost = (
        DEFEND_FATIGUE_COST
        if is_defending
        else 0
        if is_recovering
        else SPECIAL_FATIGUE_COST
        if action == "special"
        else ATTACK_FATIGUE_COST
    )
    if current_fatigue < fatigue_cost:
        return {
            "action": action,
            "round": round_number,
            "phase": "blocked",
            "reason": "not_enough_fatigue",
            "message": "Fadiga insuficiente para essa acao.",
            "hp": current_hp,
            "hp_max": hero.derive_stats().hp_max,
            "fatigue": current_fatigue,
            "fatigue_max": hero.derive_stats().fatigue_max,
            "enemy_hp": enemy_hp,
            "enemy_hp_max": enemy_profile["health"],
            "enemy_type": enemy_type,
            "enemy_name": enemy_profile["name"],
            "enemy_active": enemy_hp > 0,
            "hero_active": current_hp > 0,
        }

    fatigue_spent = min(fatigue_cost, combat.get_combatant("hero").current_fatigue)
    combat.get_combatant("hero").current_fatigue -= fatigue_spent
    player_attack: dict[str, object] = {
        "roll": None,
        "target": None,
        "success": False,
        "critical_success": False,
        "critical_failure": False,
        "damage": 0,
    }
    fatigue_recovered = 0

    if is_recovering:
        hero_combatant = combat.get_combatant("hero")
        fatigue_before = hero_combatant.current_fatigue
        fatigue_max = hero_combatant.effective_stats().fatigue_max
        hero_combatant.current_fatigue = min(
            fatigue_max,
            fatigue_before + RECOVER_FATIGUE_AMOUNT,
        )
        fatigue_recovered = hero_combatant.current_fatigue - fatigue_before
    elif not is_defending:
        roll = roll_d20() if forced_roll is None else forced_roll
        combat_action = (
            CombatAction.SURGICAL_ATTACK
            if action == "special"
            else CombatAction.ATTACK
        )
        attack = resolve_attack_action(
            action=combat_action,
            roll=roll,
            attack_value=ATTACK_TARGET,
            combatant=combat.get_combatant("hero"),
            base_damage=ATTACK_DAMAGE,
        )
        resolved = resolve_basic_attack(
            combat,
            "hero",
            "training_enemy",
            attack_success=attack.attack.test.success,
            damage=attack.final_damage or 0,
            random_roll=attack.attack.test.roll,
            modifiers={"attack": attack.attack.attack_modifier},
            effective_value=attack.attack.effective_attack_value,
        )
        player_attack = {
            "roll": attack.attack.test.roll,
            "target": attack.attack.effective_attack_value,
            "success": attack.attack.test.success,
            "critical_success": attack.attack.test.critical_success,
            "critical_failure": attack.attack.test.critical_failure,
            "damage": resolved["damage"],
        }

    hero_combatant = combat.get_combatant("hero")
    enemy_combatant = combat.get_combatant("training_enemy")
    hero_hp_after_action = hero_combatant.current_hp
    enemy_hp_after_action = enemy_combatant.current_hp
    enemy_attack: dict[str, object] = {
        "roll": None,
        "target": ENEMY_ATTACK_TARGET,
        "success": False,
        "damage": 0,
    }

    if enemy_combatant.is_active:
        enemy_roll = roll_d20()
        enemy_target = int(enemy_profile["attack_target"]) - (DEFEND_BONUS if is_defending else 0)
        enemy_resolution = resolve_attack_action(
            action=CombatAction.ATTACK,
            roll=enemy_roll,
            attack_value=enemy_target,
            combatant=enemy_combatant,
            base_damage=int(enemy_profile["attack_damage"]),
        )
        enemy_resolved = resolve_basic_attack(
            combat,
            "training_enemy",
            "hero",
            attack_success=enemy_resolution.attack.test.success,
            damage=enemy_resolution.final_damage or 0,
            random_roll=enemy_resolution.attack.test.roll,
            modifiers={"attack": enemy_resolution.attack.attack_modifier},
            effective_value=enemy_resolution.attack.effective_attack_value,
        )
        enemy_attack = {
            "roll": enemy_resolution.attack.test.roll,
            "target": enemy_resolution.attack.effective_attack_value,
            "success": enemy_resolution.attack.test.success,
            "damage": enemy_resolved["damage"],
        }

    return {
        "action": action,
        "round": round_number,
        "phase": "finished" if not enemy_combatant.is_active or not hero_combatant.is_active else "round_complete",
        "hero_active": hero_combatant.is_active,
        "roll": player_attack["roll"],
        "target": player_attack["target"],
        "success": player_attack["success"],
        "critical_success": player_attack["critical_success"],
        "critical_failure": player_attack["critical_failure"],
        "damage": player_attack["damage"],
        "fatigue_recovered": fatigue_recovered,
        "defense_bonus": DEFEND_BONUS if is_defending else 0,
        "hp": hero_combatant.current_hp,
        "hp_max": hero_combatant.effective_stats().hp_max,
        "hp_after_player_action": hero_hp_after_action,
        "fatigue": hero_combatant.current_fatigue,
        "fatigue_max": hero_combatant.effective_stats().fatigue_max,
        "enemy_hp": enemy_combatant.current_hp,
        "enemy_hp_max": enemy_profile["health"],
        "enemy_type": enemy_type,
        "enemy_name": enemy_profile["name"],
        "enemy_hp_after_player_action": enemy_hp_after_action,
        "enemy_roll": enemy_attack["roll"],
        "enemy_target": enemy_attack["target"],
        "enemy_success": enemy_attack["success"],
        "enemy_damage": enemy_attack["damage"],
        "fatigue_spent": fatigue_spent,
        "enemy_active": enemy_combatant.is_active,
    }


def get_initial_character_state() -> dict[str, object]:
    character = create_character()
    return character_state(character)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["basic", "initiative", "attack", "defend", "special", "recover"], default=None)
    parser.add_argument("--hp", type=int, default=None)
    parser.add_argument("--fatigue", type=int, default=None)
    parser.add_argument("--enemy-hp", type=int, default=None)
    parser.add_argument("--enemy-type", choices=sorted(ENEMY_PROFILES), default="training_dummy")
    parser.add_argument("--roll", type=int, default=None)
    parser.add_argument("--enemy-roll", type=int, default=None)
    parser.add_argument("--round", type=int, default=1)

    args = parser.parse_args()

    if args.action == "initiative":
        print(json.dumps(
            roll_combat_initiative(
                hero_roll=args.roll,
                enemy_roll=args.enemy_roll,
            ),
            ensure_ascii=False,
        ))
        return

    if args.action in {"attack", "defend", "special", "recover"}:
        character = create_character()
        state = execute_combat_action(
            action=args.action,
            current_hp=character.current_hp if args.hp is None else args.hp,
            current_fatigue=(
                character.current_fatigue
                if args.fatigue is None
                else args.fatigue
            ),
            enemy_hp=(
                int(ENEMY_PROFILES[args.enemy_type]["health"])
                if args.enemy_hp is None
                else args.enemy_hp
            ),
            forced_roll=args.roll,
            round_number=args.round,
            enemy_type=args.enemy_type,
        )
        print(json.dumps(state, ensure_ascii=False))
        return

    character = create_character(current_hp=args.hp, current_fatigue=args.fatigue)

    if args.action == "basic":
        execute_action(character)

    print(
        json.dumps(
            character_state(character),
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
