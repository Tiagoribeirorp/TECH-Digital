from engine.rpg.campaign.state import CampaignState, MetaProgression
from engine.rpg.character.state import Attributes, CharacterState


def make_character() -> CharacterState:
    return CharacterState(
        id="hero-1",
        name="Hero",
        race_id="human",
        attributes=Attributes(
            strength=10,
            reflexes=10,
            health=10,
            perception=10,
            intelligence=10,
            willpower=10,
            charisma=10,
        ),
    )


def test_campaign_keeps_campaign_data_separate_from_meta_progression():
    campaign = CampaignState(id="campaign-1", character=make_character())
    meta = MetaProgression()

    campaign.decisions.append({"id": "door", "choice": "open"})
    meta.mark_race_completed("human")

    assert campaign.decisions == [{"id": "door", "choice": "open"}]
    assert meta.completed_races == ["human"]
    assert meta.absolute_ending_unlocked is False


def test_meta_progression_does_not_duplicate_entries():
    meta = MetaProgression()

    meta.mark_race_completed("human")
    meta.mark_race_completed("human")
    meta.add_fragment("fragment-1")
    meta.add_fragment("fragment-1")

    assert meta.completed_races == ["human"]
    assert meta.fragments == ["fragment-1"]


def test_absolute_ending_is_explicitly_unlocked():
    meta = MetaProgression()

    meta.unlock_absolute_ending()

    assert meta.absolute_ending_unlocked is True
