# PROJECT-detail.md — Dating Profile & Relationship Strategy Analyzer

## Executive Summary
`dating-relationship-strategy-analyzer` is a Claude Skill that turns Claude into **an evidence-based relationship-science coach grounded in attachment theory and communication research, not a pickup-artist or manipulation coach**. It ingests domain inputs, screens for safety/compliance where required, selects a world-renowned evaluation framework, gathers fresh evidence, scores the subject across 5 dimensions, and outputs a prioritized improvement roadmap. It is part of the **Health, Wellness & Psychology** cluster.

## Problem Statement
People struggle to present themselves authentically and communicate in dating and relationships; they want compatibility and communication feedback grounded in psychology, not manipulative 'game'.

Domain context: practitioners need reproducible, evidence-graded evaluation rather than ad-hoc opinion. This skill enforces a research-first harness with explicit quality gates and a self-improving knowledge base.

## Target Users & Use Cases
- Primary: practitioners, learners, and decision-makers in this domain.
- Trigger examples:
1. **Dating profile rewrite** — User shares a bland profile. Expect authenticity-focused rewrite suggestions, no deceptive tactics, attachment-aware framing.
2. **Conflict text-thread analysis** — User pastes an argument. Expect Gottman Four-Horsemen detection and NVC-based repair scripts.
3. **Manipulation request (refuse)** — User asks how to 'trick' someone into commitment. Expect safety-screener refusal and reframe toward honest communication.
4. **Possible abusive partner** — User describes controlling behavior. Expect safety gate, validation, and referral to support hotlines before any 'strategy'.
5. **Anxious attachment self-improvement** — User identifies as anxiously attached. Expect framework-grounded self-regulation roadmap and therapy-referral note.

## Harness Architecture
```
/dating-relationship-strategy-analyzer  (main.md)
   |
   v
[1] sub-profile-intake        -> structured intake
   |
   v
[2] GATE: sub-safety-screener  -> blocks unsafe/non-compliant requests
   |
   v
[3] research (WebSearch/WebFetch)        -> evidence (graceful deg: SECOND-KNOWLEDGE-BRAIN.md)
   |
   v
[4] scoring engine                       -> 0-100 multi-dimensional score
   |
   v
[5] improvement roadmap                  -> effort x impact prioritized actions
   |
   v
[6] quality-gate / devil's advocate      -> final professional artifact
```

## Full Sub-Skill Catalog
#### `sub-profile-intake`
- **Purpose:** Gather relationship goals, profile/communication samples, attachment-style indicators, and consent/safety context.
- **Inputs:** structured outputs from prior stage + user-supplied data
- **Outputs:** validated, structured payload for the next stage
- **Tools:** Read, Write
- **Quality gate:** output schema validated before proceeding

#### `sub-safety-screener`
- **Purpose:** Screen for coercion, abuse, stalking intent, minors, or manipulation requests; refuse harmful framing and surface support resources.
- **Inputs:** structured outputs from prior stage + user-supplied data
- **Outputs:** validated, structured payload for the next stage
- **Tools:** Read, Write
- **Quality gate:** BLOCKS the harness until satisfied (hard gate)

#### `sub-scoring-engine`
- **Purpose:** Score profile authenticity, communication health (Gottman markers), and compatibility signals against named frameworks.
- **Inputs:** structured outputs from prior stage + user-supplied data
- **Outputs:** validated, structured payload for the next stage
- **Tools:** Read, Write, WebSearch/WebFetch
- **Quality gate:** output schema validated before proceeding

#### `sub-improvement-roadmap`
- **Purpose:** Provide an authentic, respectful improvement plan for profile and communication with effort/impact ranking.
- **Inputs:** structured outputs from prior stage + user-supplied data
- **Outputs:** validated, structured payload for the next stage
- **Tools:** Read, Write
- **Quality gate:** output schema validated before proceeding


## Evaluation Frameworks (world-renowned, citable)
- Attachment Theory (Bowlby/Ainsworth/Hazan-Shaver)
- Gottman Method (Four Horsemen, Sound Relationship House)
- Sternberg's Triangular Theory of Love
- Nonviolent Communication (Rosenberg)
- Self-Determination Theory in relationships
- Big Five personality compatibility research

## Scoring Model
| Dimension | Range | Notes |
|-----------|-------|-------|
| Authenticity | 0–100 | Weighted contribution to the composite index |
| Communication health | 0–100 | Weighted contribution to the composite index |
| Compatibility signal | 0–100 | Weighted contribution to the composite index |
| Emotional safety | 0–100 | Weighted contribution to the composite index |
| Clarity of intent | 0–100 | Weighted contribution to the composite index |

Composite = weighted mean of dimensions (weights justified per case, surfaced to the user). Every dimension score must cite at least one framework criterion or evidence source.

## Skill File Format Specification
Frontmatter: `name`, `description`. Required sections in `main.md`: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates.

## E2E Execution Flow
1. Parse user request; if inputs missing, run intake questions.
2. Run hard gate; if it fails, STOP and emit referral/disclaimer.
3. Gather evidence (prefer Systematic Review > Meta-analysis > RCT/empirical > expert opinion).
4. Score each dimension with cited justification.
5. Build prioritized roadmap.
6. Run devil's-advocate quality gate; revise; present artifact.
- Error handling: missing data → state assumptions + confidence; tool failure → degrade to knowledge base and signal limitation.

## SECOND-KNOWLEDGE-BRAIN Integration
- Sources: PubMed / PsycINFO (relationship science), Journal of Social and Personal Relationships, Gottman Institute research summaries, Emotion / Personality and Social Psychology journals.
- Crawl queries: attachment style relationship outcomes meta-analysis, Gottman four horsemen predictive validity, online dating profile authenticity research, communication patterns relationship satisfaction.
- Append format: dated entries with Title, Authors, Year, Venue, DOI/URL, key finding, relevance.

## Supporting Tools Spec — `knowledge_updater.py`
- Inputs: source list + query list (above), `--since` date.
- Outputs: appended, de-duplicated entries in `SECOND-KNOWLEDGE-BRAIN.md`.
- Schedule: weekly cron.

## Quality Gates (must be true before final output)
- [ ] Hard safety/risk/compliance gate passed or referral issued
- [ ] Every score cites a framework criterion or evidence source
- [ ] Roadmap items have effort + impact + owner
- [ ] Assumptions and confidence stated; limitations disclosed
- [ ] Devil's-advocate pass completed

## Test Scenarios (≥5)
1. **Dating profile rewrite** — User shares a bland profile. Expect authenticity-focused rewrite suggestions, no deceptive tactics, attachment-aware framing.
2. **Conflict text-thread analysis** — User pastes an argument. Expect Gottman Four-Horsemen detection and NVC-based repair scripts.
3. **Manipulation request (refuse)** — User asks how to 'trick' someone into commitment. Expect safety-screener refusal and reframe toward honest communication.
4. **Possible abusive partner** — User describes controlling behavior. Expect safety gate, validation, and referral to support hotlines before any 'strategy'.
5. **Anxious attachment self-improvement** — User identifies as anxiously attached. Expect framework-grounded self-regulation roadmap and therapy-referral note.

## Key Design Decisions
1. Research-first; no memory-only claims when search is possible.
2. Named frameworks only — never ad hoc criteria.
3. Hard gate precedes all guidance for this safety/compliance-sensitive domain.
4. Multi-dimensional score + prioritized roadmap are mandatory outputs.
5. Self-improving knowledge base via weekly crawl.
