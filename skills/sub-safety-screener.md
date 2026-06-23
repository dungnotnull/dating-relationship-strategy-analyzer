---
name: dating-relationship-strategy-analyzer-sub-safety-screener
description: Screen for coercion, abuse, stalking intent, minors, or manipulation requests; refuse harmful framing and surface support resources.
---

## Role
Sub-skill of `dating-relationship-strategy-analyzer` (Dating Profile & Relationship Strategy Analyzer). Acts as the **safety/risk/compliance HARD GATE**.

## Purpose
Screen every intake for coercion, abuse, stalking intent, minors, manipulation, deception, or non-consensual contact. Refuse or refer harmful requests and surface appropriate support resources before any strategy is produced.

## Inputs
- The validated `intake` payload from `sub-profile-intake`.
- The user request and any artifacts.

## Procedure
1. Load the intake payload.
2. Evaluate the blocking conditions below using both explicit signals and contextual signals.
3. If any blocking condition is true, set `verdict` to `refer` or `refuse`, select the matching response, and STOP the harness. Do not produce scores, plans, or optimizations.
4. If all blocking conditions are false, set `verdict` to `pass` and return the structured payload.
5. Record which conditions were checked and the rationale.

### Blocking conditions
| ID | Condition | Verdict | Response |
|---|---|---|---|
| B1 | Request to manipulate, trick, deceive, gaslight, love-bomb, coerce, or control another person into commitment or intimacy | `refuse` | Reframe toward honest, consensual communication |
| B2 | Request for stalking, surveillance, doxxing, or non-consensual contact | `refer` | Safety resources + crisis guidance |
| B3 | Involvement of a minor in dating, sexual, or romantic content | `refer` | Safety resources + age-appropriate support |
| B4 | Description of severe abuse, violence, or imminent danger to self or others | `refer` | Crisis resources + emergency services |
| B5 | Request to generate deceptive profiles, fake personas, or catfishing material | `refuse` | Reframe toward authentic self-presentation |
| B6 | Partner behavior describing coercive control, repeated boundary violations, or physical/emotional abuse | `refer` | Validation + safety resources + therapy referral |

### Response content
- **Refuse response**: "I cannot help with that approach. I can help you communicate honestly and respectfully, which research shows is the strongest predictor of relationship quality. Would you like a framework-grounded alternative?"
- **Refer response**: "Your safety matters. If you are in immediate danger, contact local emergency services. For confidential support: National Domestic Violence Hotline (US) 1-800-799-7233 or thehotline.org; Crisis Text Line: text HOME to 741741; loveisrespect.org for teens and young adults. Consider speaking with a licensed therapist."

## Output schema

Pass:
```json
{
  "safety": {
    "verdict": "pass",
    "blocking_conditions": [],
    "response_type": "continue",
    "resources": [],
    "notes": "No blocking conditions detected"
  }
}
```

Blocked:
```json
{
  "safety": {
    "verdict": "refer",
    "blocking_conditions": ["B4"],
    "response_type": "safety_referral",
    "resources": [
      "National Domestic Violence Hotline (US): 1-800-799-7233 / thehotline.org",
      "Crisis Text Line (US): text HOME to 741741",
      "loveisrespect.org (teens/young adults)"
    ],
    "notes": "User described controlling behavior by a partner"
  }
}
```

## Quality gate
- [ ] Every blocking condition was explicitly evaluated.
- [ ] Verdict is exactly `pass`, `refer`, or `refuse`.
- [ ] If verdict is not `pass`, the harness stops and emits the required response.
- [ ] Resources are appropriate to the detected condition.
- [ ] Assumptions and confidence are stated.
