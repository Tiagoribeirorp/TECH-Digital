# RPG Engine — Technical Specification

## 1. Purpose

The RPG Engine is the authoritative mechanical layer of T.E.C.H. Digital.

It resolves character rules, tests, combat, equipment effects, magic, mutations, progression, and other deterministic game mechanics.

The Narrative Engine may request a mechanical operation, but it must not decide its mechanical result.

> The AI is never the owner of the game rules.

## 2. Authority model

Player Input → Narrative/UI interpretation → RPG Engine → Rule Resolution → State Change → Narrative/World State → Presentation Engine

For direct mechanical actions: Player Action → RPG Engine → Result.

## 3. Core principles

- Rules are data-driven where practical.
- Character state is separate from character definitions.
- Equipment instances are separate from equipment definitions.
- Narrative systems may request actions but cannot override mechanical resolution.
- Optional AI may interpret natural-language intent, but it cannot invent valid rules or alter authoritative state.
- Random results must be recorded so important resolutions can be reproduced or audited.
- When the source rules do not define a value or formula, the implementation must not silently invent one.

## 4. Core state model

### CharacterState

- id
- name
- race_id
- level
- experience / progression state
- attributes
- capabilities
- talents
- limitations
- powers / mutations
- magic
- inventory
- equipment
- current_hp
- current_fatigue
- derived_stats

### AttributeState

The seven core attributes are Strength, Reflexes, Health, Perception, Intelligence, Willpower, and Charisma.

Base values and racial/other modifiers must remain distinguishable. Conceptually: base attribute + active modifiers = effective attribute.

## 5. Derived statistics

The engine owns the calculation of Reaction, Evasion, Parry, Block, Senses, Reaction Time, Speed per Turn, Movement, HP, and Fatigue.

Their formulas are maintained in SECONDARY_STATS.md.

If a formula requires an unresolved rounding or recovery rule, that rule remains a validation item rather than an invented implementation detail.

## 6. Capability resolution

The game uses the general d20 test system: roll d20 and compare against the modified capability value; success occurs when the roll is less than or equal to the effective value unless the specific rule says otherwise.

For resisted tests, each participant produces a margin and the higher margin wins.

The engine must expose the complete resolution record.

## 7. Combat

Combat is a subsystem of the RPG Engine.

CombatState should contain participants, round, phase, initiative_order, declared_actions, resolved_actions, distances, temporary_modifiers, active_effects, combat_log, and status.

Combat phases are Initiative, Declaration, Execution, Resolution, and Next Round/End.

The T.E.C.H. combat system uses approximately five-second rounds. Declaration occurs from slower to faster participants. Execution occurs from faster to slower participants. Initiative is not rerolled every round.

The complete action catalogue and unresolved combat rules are maintained in COMBAT_SYSTEM.md.

## 8. Equipment

Equipment is data-driven. Definitions describe what an item is; instances represent an actual owned item.

EquipmentDefinition → EquipmentInstance → Character inventory/equipment slots.

Equipment can affect effective attributes, derived statistics, combat actions, load, and other rules.

The engine must recalculate dependent values rather than permanently modifying base attributes.

The complete equipment model is maintained in EQUIPMENT_SYSTEM.md.

## 9. Magic

Magic is a subsystem separate from mutation.

The engine must support magic definitions, requirements, costs, effects, duration, range, maintained effects, artifacts and Arcane Runes where defined, tests, and fatigue interactions.

Magic can be used in combat or outside combat.

The complete magic specification is maintained in MAGIC_SYSTEM.md.

## 10. Mutations

Mutations represent powers resulting from genetic/DNA alterations.

The mutation subsystem must support mutation definitions, requirements, levels, fatigue costs, range, duration, damage/effects, type, Speed per Turn where applicable, maintained powers, and evolution.

Activation uses the applicable Intelligence test defined by the source rules. Critical results and fatigue consequences must follow the source rules.

The complete mutation specification is maintained in MUTATION_SYSTEM.md.

## 11. Progression

Progression is a separate subsystem. It owns level, PE, attribute improvements, new talents, new powers/magic, power/magic evolution, capability improvements, and HP/Fatigue improvements.

The current source contains more than one progression table/economy that has not yet been reconciled. The engine must preserve that inconsistency as a design-validation item rather than silently choosing one interpretation.

See PROGRESSION_SYSTEM.md.

## 12. Deterministic resolution

Important mechanical operations should produce a resolution record containing id, source, action, actor, target, random_roll, modifiers, effective_value, result, consequences, and sequence/timestamp.

This allows debugging, replay-oriented testing, and transparent combat logs.

## 13. State mutation

The preferred pattern is: Input → Validate → Resolve → Create Result → Apply State Changes → Emit Events.

Examples of events include AttackResolved, DamageApplied, EquipmentEquipped, MagicCast, MutationActivated, ExperienceAwarded, and QuestStateChanged.

Events connect the RPG Engine to Narrative, World, UI, audio, and presentation without making those systems authoritative over the rules.

## 14. Narrative integration

The Narrative Engine may submit a proposed action. The RPG Engine validates and resolves it, then returns a result that can produce a narrative consequence.

Example: a player says they try to sneak past a guard; the narrative layer proposes a Furtividade test; the RPG Engine resolves the d20 test; the Narrative Engine applies an authored consequence.

The narrative layer must not directly assign damage, XP, success, or stat changes without passing through the appropriate rule system.

## 15. Optional AI integration

AI is an optional layer.

It may assist with natural-language intent interpretation, dialogue variation, descriptive text, NPC conversational responses, and selecting among authored narrative options.

It must not be authoritative for character statistics, damage, XP, item effects, legal actions, spell/power costs, combat results, or persistent world state.

The game must remain playable when the AI layer is unavailable.

## 16. Save/load contract

Persistent state must be serializable.

At minimum, a campaign save should preserve CharacterState, inventory and equipment instances, quest state, relevant NPC state, faction/world state, decisions, discoveries, and active campaign consequences.

The global/meta profile should remain separate from a campaign save.

## 17. Validation and errors

Every requested operation should be validated before state mutation.

Examples: CanEquip, CanUseMagic, CanActivateMutation, CanPerformAction, HasResource, and MeetsRequirement.

Invalid operations should return structured failures rather than silently changing state.

## 18. Testing strategy

The RPG Engine should be testable without launching the full Godot presentation layer.

Tests should cover d20 resolution, modifiers, resisted tests, derived statistics, equipment modifiers, load penalties, combat order, combat actions, damage, fatigue, magic, mutations, progression, and save/load serialization.

## 19. Implementation boundary

Godot is responsible for rendering, UI, animation, audio, input, camera, scene management, presentation, and platform integration.

The RPG Engine is responsible for rules, state, calculations, validation, resolution, mechanical outcomes, and persistence-facing game state.

The boundary should remain explicit.

## 20. Current implementation status

The specification phase has documented Character System, Races, Attributes/Secondary Stats, Skills, Progression, Combat, Equipment, Magic, and Mutations.

Before gameplay code is treated as the definitive implementation, remaining source validation should cover unresolved combat/equipment/magic/mutation details and contradictions in the original rules.

## 21. Next technical milestone

The next implementation milestone is the first headless RPG Engine prototype:

1. Create CharacterState.
2. Create attributes and derived stats.
3. Implement d20 tests.
4. Implement one capability.
5. Implement HP and Fatigue.
6. Implement one weapon.
7. Implement one enemy.
8. Implement one basic attack.
9. Implement combat round flow.
10. Implement XP/progression.
11. Serialize and load the state.
12. Expose the result to Godot.

The first prototype should be small, deterministic where practical, and playable from start to finish before expanding content.