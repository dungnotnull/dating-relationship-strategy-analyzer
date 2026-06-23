---
name: dating-relationship-strategy-analyzer-sub-improvement-roadmap
description: Provide an authentic, respectful improvement plan for profile and communication with effort/impact ranking.
---

## Role
Sub-skill of `dating-relationship-strategy-analyzer` (Dating Profile & Relationship Strategy Analyzer). Acts as the **roadmap stage**.

## Purpose
Convert the scorecard into a prioritized, actionable improvement plan anchored to named frameworks. The plan must be authentic, respectful, and safe.

## Inputs
- Validated `intake` payload.
- Passed `safety` payload.
- `scorecard` payload.

## Procedure
1. Identify dimensions with score <70 and high-leverage dimensions where a small effort yields a large impact.
2. Generate concrete actions grounded in the frameworks used for scoring.
3. Score each action:
   - Effort: 1 (low) to 5 (high)
   - Impact: 1 (low) to 5 (high)
   - Priority score = Impact / Effort
4. Sort descending by priority score. Surface the top 5 items.
5. Assign an owner (`self`, `partner-with-consent`, `therapist`, `both`).
6. State expected effect and a resource/citation.

### Effort scale
| Score | Effort level | Examples |
|---|---|---|
| 1 | One try, same conversation | Swap one generic line for a values-based sentence |
| 2 | A few tries over one week | Add one NVC-style repair script |
| 3 | Daily practice for 2-4 weeks | Soft-start journaling, self-soothing routine |
| 4 | Multi-week skill building | Attachment-based therapy or structured communication coaching |
| 5 | Long-term identity/relationship change | Shift core attachment pattern, leave an unsafe relationship |

### Impact scale
| Score | Impact level | Examples |
|---|---|---|
| 1 | Marginal | Minor wording tweak with low signal value |
| 2 | Noticeable | Reduces one Four Horsemen marker |
| 3 | Meaningful | Improves emotional safety or clarity of intent |
| 4 | Large | Reframes entire profile or conflict pattern |
| 5 | Transformative | Resolves safety concern or core compatibility mismatch |

### Output schema
```json
{
  "roadmap": {
    "items": [
      {
        "rank": 1,
        "action": "Rewrite the profile opening with one values-based, specific anecdote and one honest relationship goal.",
        "dimension": "authenticity",
        "framework": "Attachment Theory + Self-Determination Theory",
        "effort": 2,
        "impact": 4,
        "priority_score": 2.0,
        "owner": "self",
        "expected_effect": "Higher signal-to-noise ratio; attracts partners who share stated values.",
        "resources": ["Hazan & Shaver (1987); Levine & Heller (2010)"]
      },
      {
        "rank": 2,
        "action": "Replace accusatory 'you' statements with observation+feeling+need+request scripts during the next conflict.",
        "dimension": "communication_health",
        "framework": "Gottman Method + Nonviolent Communication",
        "effort": 3,
        "impact": 4,
        "priority_score": 1.33,
        "owner": "self",
        "expected_effect": "Reduces escalation and increases repair attempts.",
        "resources": ["Gottman & Levenson (1992); Rosenberg (2003)"]
      }
    ],
    "summary": "Top priorities focus on authenticity and communication health because they are high-impact, medium-effort levers."
  }
}
```

## Quality gate
- [ ] Scorecard is loaded and all dimensions are represented.
- [ ] Every roadmap item cites a framework.
- [ ] Effort and impact are integers in 1-5.
- [ ] Priority score is computed as impact / effort.
- [ ] Owners are explicit and safe.
- [ ] Summary explains the prioritization logic.
