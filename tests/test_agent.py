from pathlib import Path

from finn.agent import FinnAgent


ROOT = Path(__file__).resolve().parents[1]


def test_agent_answers_sleep_question_with_source() -> None:
    agent = FinnAgent(
        kb_path=ROOT / "data" / "knowledge_base.md",
        user_profile_path=ROOT / "data" / "sample_user_profile.json",
    )

    answer = agent.answer("I have been sleeping around 5 hours. What can I do?")

    assert answer.category == "wellness_answer"
    assert "sleep" in answer.response.lower()
    assert answer.sources
    assert answer.sources[0].title == "Sleep Basics"


def test_agent_declines_medication_question() -> None:
    agent = FinnAgent(
        kb_path=ROOT / "data" / "knowledge_base.md",
        user_profile_path=ROOT / "data" / "sample_user_profile.json",
    )

    answer = agent.answer("Should I take 10mg melatonin every night?")

    assert answer.category == "medication_request"
    assert not answer.sources
    assert "cannot recommend" in answer.response
