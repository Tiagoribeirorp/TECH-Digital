# Dice Resolution & Presentation Contract

## Purpose

Define the boundary between mechanical dice resolution and the visual dice experience.

## Authority

The RPG Engine is authoritative.

The Presentation Engine may animate and display a roll, but it must not decide the number rolled or the mechanical outcome.

Flow:

Player action
→ RPG Engine requests d20
→ random result is recorded
→ RPG Engine resolves the test
→ result/consequences are returned
→ Presentation Engine animates/displays the recorded roll
→ Narrative/UI presents the consequence

## Player-facing roll

For an interactive roll, the UI may present a D20 and a "Roll" action.

The player's interaction starts the resolution, but the visual animation is not the source of randomness. The authoritative roll belongs to the RPG Engine.

This preserves fairness, replayability, debugging, and headless testing.

## Standard test

The current engine rule is:

- Roll d20.
- Compare the roll with the effective capability value.
- Roll <= effective value = success.
- Natural 1 = critical success.
- Natural 20 = critical failure.

The source material supports the <= success rule. Critical handling is part of the current engine prototype and remains subject to source validation where the complete critical consequences are not defined.

## Resisted test

Each participant produces a test result.

Margin = effective value - roll.

The higher margin wins. A tie remains a tie unless a specific rule defines another outcome.

## Attack reaction presentation

For combat:

1. Attack is announced.
2. The defender receives a reaction window.
3. Valid reactions are presented according to the character's current state.
4. The defender chooses a reaction.
5. The RPG Engine resolves the attack and defense.
6. The Presentation Engine shows the relevant dice and result.

Example:

> Enemy announces an attack.
>
> **How do you react?**
>
> - Dodge
> - Parry
> - Block
> - Other valid authored reaction
>
> The chosen reaction is stored before attack resolution.

## Important implementation rule

Do not implement the visual die as a separate random system.

Bad:
UI rolls 8 → Engine is told the result is 8

Correct:
Engine rolls 8 → UI animates/displays the result 8

The visual die is therefore presentation of an authoritative mechanical event.

## Future Godot integration

Godot will eventually own:

- die model/animation;
- input;
- camera;
- sound;
- timing;
- result presentation;
- combat UI.

The RPG Engine will own:

- d20 generation;
- validation;
- test resolution;
- resisted-test resolution;
- critical flags;
- consequences;
- resolution records.

This keeps the game playable and testable without Godot.
