"""Small headless end-to-end scenario for the RPG Engine.

This is a development smoke test, not a game rules fixture. Damage is supplied
explicitly because the authoritative attack/damage formula is still unresolved.
"""

from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.combat.engine import begin_execution, resolve_basic_attack, roll_initiative, start_combat
from engine.rpg.progression.state import ProgressionState


def run_demo() -> dict[str, object]:
    hero = CharacterState(
        id="hero", name="Heroi", race_id="human",
        attributes=Attributes(12, 12, 12, 12, 12, 12, 12),
    )
    enemy = CharacterState(
        id="enemy", name="Inimigo", race_id="test",
        attributes=Attributes(10, 10, 10, 10, 10, 10, 10),
    )
    progression = ProgressionState()
    combat = start_combat([hero, enemy])
    roll_initiative(combat, iter([10, 1]).__next__)
    begin_execution(combat)
    resolve_basic_attack(combat, "hero", "enemy", attack_success=True, damage=10)
    progression.add_evolution_points(1)
    return {
        "combat_status": combat.status,
        "enemy_hp": combat.get_combatant("enemy").current_hp,
        "hero_pe": progression.spendable_evolution_points,
        "log_entries": len(combat.combat_log),
    }
