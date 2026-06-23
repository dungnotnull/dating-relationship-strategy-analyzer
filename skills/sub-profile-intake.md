---
name: dating-relationship-strategy-analyzer-sub-profile-intake
description: Gather relationship goals, profile/communication samples, attachment-style indicators, and consent/safety context.
---

## Role
Sub-skill of `dating-relationship-strategy-analyzer` (Dating Profile & Relationship Strategy Analyzer). Acts as the **pre-gate intake stage**.

## Purpose
Collect the minimum structured inputs required to run the safety gate, select an evaluation framework, and produce a scored roadmap. Do not proceed past this stage until the payload passes validation.

## Inputs
- The user request and any artifacts supplied by the user.
- Structured output from the previous harness stage (empty at workflow start).

## Procedure
1. Classify the request into one supported type:
   - `profile_rewrite`
   - `conflict_analysis`
   - `self_improvement`
   - `compatibility_question`
   - `safety_concern`
   - `general`
2. Collect the required fields below. If any field is missing or ambiguous, ask a targeted follow-up question and stop further processing until it is supplied.
3. Validate the payload against the output schema and the validation rules.
4. Mask any direct identifiers found in `communication_sample` (full names, addresses, phone numbers, email addresses, social handles) before producing the output.
5. Record assumptions and confidence.

### Required fields
| Field | Description | Allowed values |
|---|---|---|
| `request_type` | Classification of the user request | `profile_rewrite`, `conflict_analysis`, `self_improvement`, `compatibility_question`, `safety_concern`, `general` |
| `relationship_goal` | What the user wants from this interaction | free text, 500 chars max |
| `age_group` | Whether all described parties are adults | `adult`, `minor`, `unknown` |
| `attachment_style_self` | User's self-reported attachment style | `secure`, `anxious`, `avoidant`, `disorganized`, `unknown` |
| `communication_sample` | Profile text, message thread, or conflict transcript | free text, 8000 chars max |
| `context` | Where/how the sample is used (app, in-person, etc.) | free text, 500 chars max |
| `consent_context` | How third-party data was shared (with consent, public, own data only, etc.) | free text, 500 chars max |

### Validation rules
- `request_type`, `relationship_goal`, `age_group`, and `communication_sample` are mandatory.
- `age_group == minor` must be routed to the safety gate with verdict `refer`.
- `communication_sample` must not contain unmasked direct identifiers. If it does, mask them and add an assumption.
- If `communication_sample` describes violence, coercion, stalking, or non-consensual behavior, set `request_type` to `safety_concern` and route to the safety gate.

## Output schema
Return exactly one JSON object:

```json
{
  "intake": {
    "request_type": "profile_rewrite",
    "relationship_goal": "Find a long-term partner who values emotional intimacy",
    "age_group": "adult",
    "attachment_style_self": "anxious",
    "communication_sample": "Hey, I am Alex. I like hiking, reading, and deep conversations...",
    "context": "Hinge dating profile",
    "consent_context": "My own profile; no third-party data",
    "additional_notes": "User worries about sounding too eager"
  },
  "validation": {
    "passed": true,
    "missing": [],
    "flags": [],
    "assumptions": ["User is writing about themselves"],
    "confidence": "high"
  }
}
```

## Quality gate
- [ ] `request_type` is one of the supported values.
- [ ] All mandatory fields are present and non-empty.
- [ ] `age_group == minor` is explicitly flagged for the safety gate.
- [ ] Direct identifiers in `communication_sample` are masked.
- [ ] Output JSON matches the schema above.
- [ ] Assumptions and confidence are stated.
