# ADR 001: Framework Selection and Scoring Scale

## Status
Accepted

## Context
`dating-relationship-strategy-analyzer` must produce reproducible, evidence-based assessments of dating profiles and relationship communication. We needed to decide:

1. Which frameworks to anchor judgments to.
2. How many scoring dimensions to expose.
3. What scale to use so results are comparable across the Health, Wellness & Psychology cluster.
4. How to prioritize roadmap actions.

## Decision

### Frameworks
We anchor all judgments to six named, citable frameworks:

- Attachment Theory (Bowlby/Ainsworth/Hazan-Shaver)
- Gottman Method (Four Horsemen, Sound Relationship House)
- Sternberg's Triangular Theory of Love
- Nonviolent Communication (Rosenberg)
- Self-Determination Theory in relationships
- Big Five personality compatibility research

No ad hoc criteria are allowed. Every dimension score and roadmap action must cite one of these frameworks or an entry from `SECOND-KNOWLEDGE-BRAIN.md`.

### Five Dimensions
The scorecard covers:

1. **Authenticity** — values-based, bounded self-disclosure.
2. **Communication health** — absence of Gottman Four Horsemen + presence of NVC components.
3. **Compatibility signal** — values/goals/intent alignment per Sternberg and Big Five research.
4. **Emotional safety** — safe-haven behavior, consent, validation.
5. **Clarity of intent** — explicit, direct relationship intent and requests.

### 0-100 Scale
Each dimension is scored 0-100. The composite is a weighted mean with transparent weights. This scale aligns with sibling skills in the Health, Wellness & Psychology cluster.

Default weights:

| Dimension | Weight |
|---|---|
| Authenticity | 0.25 |
| Communication health | 0.25 |
| Compatibility signal | 0.15 |
| Emotional safety | 0.20 |
| Clarity of intent | 0.15 |

### Effort/Impact Prioritization
Roadmap actions are scored effort (1-5) and impact (1-5). Priority = impact / effort. This favors high-leverage, low-effort actions first while still surfacing transformative actions when safety demands it.

## Consequences

- Positive: Scores are transparent, comparable, and defensible. Users can see exactly which framework supports each judgment.
- Positive: The hard safety gate runs before any scoring, preventing harmful guidance.
- Trade-off: The five-dimensional model may not capture every nuance of a relationship. The skill must disclose assumptions and confidence.
- Trade-off: Default weights are general; users may need to adjust them for specific contexts, which the skill supports by surfacing weights explicitly.

## References
- Hazan & Shaver (1987). Romantic love conceptualized as an attachment process.
- Sternberg (1986). A triangular theory of love.
- Gottman & Levenson (1992). Marital processes predictive of later dissolution.
- Rosenberg (2003). Nonviolent Communication: A Language of Life.
- Deci & Ryan (2000). Self-determination theory.
