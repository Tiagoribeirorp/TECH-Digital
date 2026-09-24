"""Resolution log helpers."""

from engine.rpg.core.resolution import ResolutionRecord


def append_resolution(
    log: list[ResolutionRecord],
    record: ResolutionRecord,
) -> ResolutionRecord:
    """Append a structured resolution and assign a deterministic sequence."""
    sequenced = ResolutionRecord(
        source=record.source,
        action=record.action,
        actor_id=record.actor_id,
        target_id=record.target_id,
        random_roll=record.random_roll,
        modifiers=dict(record.modifiers),
        effective_value=record.effective_value,
        result=record.result,
        consequences=dict(record.consequences),
        sequence=len(log) + 1,
        id=record.id,
    )
    log.append(sequenced)
    return sequenced
