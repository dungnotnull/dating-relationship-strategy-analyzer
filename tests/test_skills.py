import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).parent.parent / "skills"

REQUIRED_SKILLS = [
    "main.md",
    "sub-profile-intake.md",
    "sub-safety-screener.md",
    "sub-scoring-engine.md",
    "sub-improvement-roadmap.md",
]

SUB_SKILL_SLUGS = [
    "sub-profile-intake",
    "sub-safety-screener",
    "sub-scoring-engine",
    "sub-improvement-roadmap",
]


@pytest.mark.parametrize("name", REQUIRED_SKILLS)
def test_skill_has_required_frontmatter(name):
    text = (SKILL_DIR / name).read_text(encoding="utf-8")
    assert text.startswith("---"), f"{name} missing opening frontmatter"
    assert "name:" in text, f"{name} missing name field"
    assert "description:" in text, f"{name} missing description field"


@pytest.mark.parametrize("name", REQUIRED_SKILLS)
def test_skill_has_quality_gate_section(name):
    text = (SKILL_DIR / name).read_text(encoding="utf-8")
    assert re.search(r"## Quality [Gg]ate", text), f"{name} missing quality gate section"
    assert re.search(r"- \[ ?\] ", text), f"{name} has no unchecked checklist items"


@pytest.mark.parametrize("name", REQUIRED_SKILLS[1:])
def test_sub_skill_declares_role_and_purpose(name):
    text = (SKILL_DIR / name).read_text(encoding="utf-8")
    assert "## Role" in text, f"{name} missing Role section"
    assert "## Purpose" in text, f"{name} missing Purpose section"
    assert "## Procedure" in text, f"{name} missing Procedure section"
    assert "## Output schema" in text, f"{name} missing Output schema section"


def test_main_references_all_sub_skills():
    text = (SKILL_DIR / "main.md").read_text(encoding="utf-8")
    for slug in SUB_SKILL_SLUGS:
        assert slug in text, f"main.md does not reference {slug}"


def test_main_declares_workflow_and_tools():
    text = (SKILL_DIR / "main.md").read_text(encoding="utf-8")
    assert "## Workflow (Harness Flow)" in text
    assert "## Tools" in text
    assert "## Output Format" in text
    assert "## Quality Gates" in text


def test_safety_screener_lists_blocking_conditions():
    text = (SKILL_DIR / "sub-safety-screener.md").read_text(encoding="utf-8")
    assert "B1" in text
    assert "B2" in text
    assert "verdict" in text
    assert "refer" in text
    assert "refuse" in text


def test_scoring_engine_has_five_dimensions():
    text = (SKILL_DIR / "sub-scoring-engine.md").read_text(encoding="utf-8")
    for dim in ["authenticity", "communication_health", "compatibility_signal", "emotional_safety", "clarity_of_intent"]:
        assert dim in text, f"sub-scoring-engine.md missing {dim}"


def test_roadmap_has_effort_and_impact():
    text = (SKILL_DIR / "sub-improvement-roadmap.md").read_text(encoding="utf-8")
    assert "effort" in text
    assert "impact" in text
    assert "priority_score" in text
