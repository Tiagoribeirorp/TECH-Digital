from pathlib import Path

from engine.rpg.campaign.state import CampaignState, MetaProgression
from engine.rpg.character.state import Attributes, CharacterState
from engine.rpg.persistence.campaign_save import load_full_state, save_full_state


def test_full_campaign_round_trip(tmp_path: Path):
    character = CharacterState(
        id="hero-1",
        name="Hero",
        race_id="human",
        attributes=Attributes(10, 11, 12, 13, 14, 15, 16),
        current_hp=9,
        current_fatigue=14,
        skill_values={"combat": 4},
        talents=["talent-1"],
    )
    campaign = CampaignState(id="campaign-1", character=character)
    campaign.decisions.append({"id": "door", "choice": "open"})
    campaign.discoveries.append("fragment-1")
    campaign.active_consequences.append({"id": "alarm", "active": True})

    meta = MetaProgression()
    meta.mark_race_completed("human")
    meta.add_fragment("fragment-1")
    meta.add_ending("ending-1")
    meta.unlock_absolute_ending()

    path = tmp_path / "save.json"
    save_full_state(path, campaign, meta)
    loaded_campaign, loaded_meta = load_full_state(path)

    assert loaded_campaign.id == campaign.id
    assert loaded_campaign.character.attributes.as_dict() == character.attributes.as_dict()
    assert loaded_campaign.character.current_hp == 9
    assert loaded_campaign.decisions == campaign.decisions
    assert loaded_campaign.discoveries == campaign.discoveries
    assert loaded_campaign.active_consequences == campaign.active_consequences
    assert loaded_meta.completed_races == ["human"]
    assert loaded_meta.fragments == ["fragment-1"]
    assert loaded_meta.endings_discovered == ["ending-1"]
    assert loaded_meta.absolute_ending_unlocked is True
