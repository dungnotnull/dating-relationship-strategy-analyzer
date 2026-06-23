import json
from pathlib import Path

import pytest

SCENARIOS_PATH = Path(__file__).parent / "scenarios.json"


def _load_scenarios():
    with open(SCENARIOS_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def _classify_gate(text: str) -> str:
    lower = text.lower()
    manipulation = ["trick", "deceive", "manipulate", "gaslight", "love-bomb", "coerce", "control", "fake", "catfish"]
    abuse = ["abuse", "violent", "controlling", "checks my phone", "hurt themselves", "stalk", "non-consensual"]
    minor = ["16", "minor", "teenager", "underage"]
    if any(w in lower for w in manipulation):
        return "refuse"
    if any(w in lower for w in abuse):
        return "refer"
    if any(w in lower for w in minor):
        return "refer"
    return "pass"


SCENARIOS = _load_scenarios()


def test_at_least_five_scenarios():
    assert len(SCENARIOS) >= 5


def test_each_scenario_has_required_fields():
    for s in SCENARIOS:
        assert "id" in s
        assert "name" in s
        assert "input" in s
        assert "expected_verdict" in s
        assert "expected_frameworks" in s
        assert "expected_dimensions" in s


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda s: f"{s['id']}-{s['name']}")
def test_expected_verdict_matches_classifier(scenario):
    predicted = _classify_gate(scenario["input"])
    assert predicted == scenario["expected_verdict"], (
        f"Scenario {scenario['id']} ({scenario['name']}): classifier said {predicted}, expected {scenario['expected_verdict']}"
    )


def test_scenarios_cover_all_dimensions():
    all_dims = {"authenticity", "communication_health", "compatibility_signal", "emotional_safety", "clarity_of_intent"}
    covered = set()
    for s in SCENARIOS:
        covered.update(s.get("expected_dimensions", []))
    assert all_dims.issubset(covered), f"Dimensions not covered: {all_dims - covered}"
