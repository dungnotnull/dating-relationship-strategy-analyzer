# cluster-integration.md - Health, Wellness & Psychology Cross-Skill Contract

`dating-relationship-strategy-analyzer` belongs to the **Health, Wellness & Psychology** (`health-wellness`) cluster. This document defines how it shares and reuses sub-skills, scoring scales, and safety contracts with sibling skills.

## Shared Sub-Skills

The following sub-skills are published as reusable, schema-bound stages. Sibling skills may invoke them by loading the corresponding `skills/sub-*.md` file.

| Sub-skill | Reuse contract | Cluster siblings likely to reuse |
|---|---|---|
| `sub-profile-intake` | Structured relationship/communication intake with age-group, consent, and attachment-style fields. | Couples-communication coach, breakup-recovery coach, intimacy-education skill |
| `sub-safety-screener` | Hard gate for coercion, abuse, stalking, minors, and manipulation. | Any relationship, sex-ed, or mental-health skill |
| `sub-scoring-engine` | 0-100 five-dimensional scorecard with cited frameworks. | Compatibility tools, communication-quality audits, self-improvement trackers |
| `sub-improvement-roadmap` | Effort/impact-prioritized action list with owners and expected effects. | Wellness planners, therapy-prep skills, conflict-resolution skills |

## Scoring Scale Alignment

All cluster skills that produce numeric assessments should align on this scale to avoid user confusion:

| Scale | Interpretation | Color signal |
|---|---|---|
| 0-39 | Significant concern or blocker | Red |
| 40-69 | Mixed signals; room for improvement | Amber |
| 70-89 | Strong, healthy pattern | Green |
| 90-100 | Exceptional, model pattern | Dark green |

`dating-relationship-strategy-analyzer` applies this scale to its five dimensions and surfaces the composite as a weighted mean.

## Framework Canon

Sibling skills should prefer the same named frameworks where the domain overlaps:

- Attachment Theory (Bowlby/Ainsworth/Hazan-Shaver)
- Gottman Method (Four Horsemen, Sound Relationship House)
- Sternberg's Triangular Theory of Love
- Nonviolent Communication (Rosenberg)
- Self-Determination Theory in relationships
- Big Five personality compatibility research

## Safety Gate Reuse

The `sub-safety-screener` hard gate is cluster-safe: it screens for minors, coercion, abuse, and non-consensual behavior regardless of the specific health/wellness topic. Sibling skills may copy the gate verbatim or import its blocking-condition table into their own safety stage.

## Knowledge Base Sharing

`SECOND-KNOWLEDGE-BRAIN.md` is the cluster's relationship-science repository. Sibling skills may:

1. Read it for authoritative evidence in relationship/communication domains.
2. Contribute new dated entries using the same append format and hash convention.
3. Run `tools/knowledge_updater.py` to refresh all shared knowledge bases.

## I/O Schema Convention

All sub-skills use JSON payloads with a top-level stage key and a `validation`/`quality` object. Sibling skills should preserve this envelope so that stages can be chained.

Example envelope:

```json
{
  "intake": { ... },
  "validation": { "passed": true, "missing": [], "assumptions": [], "confidence": "high" }
}
```

## Versioning

- **Current cluster alignment version:** 1.0
- **Last reviewed:** 2026-06-23
- **Owner skill:** `dating-relationship-strategy-analyzer`
