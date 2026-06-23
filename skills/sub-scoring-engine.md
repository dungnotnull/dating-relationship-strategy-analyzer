---
name: dating-relationship-strategy-analyzer-sub-scoring-engine
description: Score profile authenticity, communication health (Gottman markers), and compatibility signals against named frameworks.
---

## Role
Sub-skill of `dating-relationship-strategy-analyzer` (Dating Profile & Relationship Strategy Analyzer). Acts as the **scoring stage**.

## Purpose
Produce a reproducible 0-100 scorecard across five dimensions. Every dimension score must be anchored to a named, citable framework criterion and to evidence from the knowledge base or live sources.

## Inputs
- Validated `intake` payload.
- Passed `safety` payload.
- Evidence from `SECOND-KNOWLEDGE-BRAIN.md` or live search results.

## Procedure
1. Select the dominant frameworks based on `request_type`:
   - `profile_rewrite`: Attachment Theory, Self-Determination Theory (autonomy), Big Five personality compatibility research
   - `conflict_analysis`: Gottman Method, Nonviolent Communication
   - `self_improvement`: Attachment Theory, Self-Determination Theory
   - `compatibility_question`: Sternberg's Triangular Theory of Love, Big Five compatibility, Attachment Theory
   - `safety_concern`: scoring is skipped; safety gate handles the case
   - `general`: use the framework most relevant to the stated goal
2. For each dimension, assign a 0-100 score using the rubric below.
3. Cite a specific framework criterion and, when available, an evidence source (author/year/DOI).
4. Compute composite = weighted mean. Default weights: Authenticity 0.25, Communication health 0.25, Compatibility signal 0.15, Emotional safety 0.20, Clarity of intent 0.15.
5. Surface the weights, assumptions, and confidence.

### Scoring rubric
| Dimension | Framework anchor | 0-40 band | 41-70 band | 71-100 band |
|---|---|---|---|---|
| Authenticity | Attachment secure base + Self-Determination autonomy | Generic, performative, disguised, or empty persona | Some personal detail but inconsistent, guarded, or approval-seeking | Specific, values-based, vulnerable yet bounded; clear self-presentation |
| Communication health | Gottman Four Horsemen absence + NVC components | Criticism, contempt, defensiveness, stonewalling, or blame present | Neutral but lacks repair, needs, or explicit requests | Soft start, repair attempts, observation+feeling+need+request |
| Compatibility signal | Sternberg intimacy/passion/commitment + Big Five | Mismatched values/goals or no signal | Partial fit, some shared goals, ambiguous intent | Clear alignment on values, goals, and relationship intent |
| Emotional safety | Gottman safe-haven + Attachment safe-haven | Dismissive, invalidating, threatening, or boundary-violating | Polite but lacks validation, consent check, or repair | Validating, respects boundaries, consent-affirming, emotionally responsive |
| Clarity of intent | NVC request clarity + commitment/intent explicitness | Ambiguous, mixed signals, passive, or hinting | Vague but hints at intent; indirect request | Explicit, direct request/statement of intent; mutual understanding |

### Output schema
```json
{
  "scorecard": {
    "dimensions": {
      "authenticity": {
        "score": 68,
        "weight": 0.25,
        "justification": "Profile includes personal hobbies but remains approval-seeking and avoids values.",
        "criterion": "Secure-base self-disclosure and autonomy support (Self-Determination Theory)",
        "source": "Hazan & Shaver (1987); Deci & Ryan (2000)"
      },
      "communication_health": {
        "score": 62,
        "weight": 0.25,
        "justification": "Messages are neutral but lack repair attempts and explicit needs.",
        "criterion": "Absence of Gottman Four Horsemen + presence of NVC observation/feeling/need/request",
        "source": "Gottman & Levenson (1992); Rosenberg (2003)"
      },
      "compatibility_signal": {
        "score": 55,
        "weight": 0.15,
        "justification": "Stated goals are broad; no clear values alignment signal.",
        "criterion": "Sternberg intimacy/passion/commitment balance + Big Five values alignment",
        "source": "Sternberg (1986)"
      },
      "emotional_safety": {
        "score": 70,
        "weight": 0.20,
        "justification": "No contempt or threats; boundary language is implicit.",
        "criterion": "Safe-haven behavior and absence of coercive control",
        "source": "Gottman & Levenson (1992)"
      },
      "clarity_of_intent": {
        "score": 50,
        "weight": 0.15,
        "justification": "Goal is stated but the ask is indirect.",
        "criterion": "NVC clear request + explicit relationship intent",
        "source": "Rosenberg (2003)"
      }
    },
    "composite": 62.55,
    "weights": {
      "authenticity": 0.25,
      "communication_health": 0.25,
      "compatibility_signal": 0.15,
      "emotional_safety": 0.20,
      "clarity_of_intent": 0.15
    },
    "confidence": "medium",
    "assumptions": ["User self-report is accurate", "Sample is representative of typical communication"]
  }
}
```

## Quality gate
- [ ] Intake and safety payloads are loaded.
- [ ] Every dimension score cites a named framework criterion.
- [ ] Scores are integers in 0-100.
- [ ] Weights sum to 1.0 within rounding error.
- [ ] Composite is computed as weighted mean.
- [ ] Confidence and assumptions are stated.
