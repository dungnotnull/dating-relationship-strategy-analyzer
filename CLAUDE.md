# CLAUDE.md - Dating Profile & Relationship Strategy Analyzer (idea 111)

## Skill Identity
- **Name / slug:** `dating-relationship-strategy-analyzer`
- **Tagline:** Dating Profile & Relationship Strategy Analyzer
- **Source idea:** #111 (`ideas.md`)
- **Cluster:** Health, Wellness & Psychology (`health-wellness`)
- **Current phase:** Phase 5 - Integration & Cross-Skill Wiring complete

## Problem This Skill Solves
People struggle to present themselves authentically and communicate in dating and relationships; they want compatibility and communication feedback grounded in psychology, not manipulative "game".

This skill becomes **an evidence-based relationship-science coach grounded in attachment theory and communication research, not a pickup artist or manipulation coach**. It is research-first, grounds every score in named world-renowned frameworks, challenges its own assumptions before concluding, and produces a professional artifact: a multi-dimensional score plus a prioritized improvement roadmap.

## Harness Flow Summary
1. **Intake** - `sub-profile-intake` gathers structured inputs.
2. **Gate / framework** - safety/risk/compliance gate runs, then the correct evaluation framework is selected.
3. **Research** - WebSearch/WebFetch enrich evidence from authoritative sources (graceful degradation to `SECOND-KNOWLEDGE-BRAIN.md` if unavailable).
4. **Scoring** - `sub-scoring-engine` produces a 0-100 multi-dimensional score.
5. **Roadmap** - prioritized improvement plan (effort x impact).
6. **Quality gate** - devil's advocate review before final output.

**SAFETY GATE:** `sub-safety-screener` MUST pass before any guidance is emitted.

## Sub-skills
- `skills/sub-profile-intake.md` - Gather relationship goals, profile/communication samples, attachment-style indicators, and consent/safety context.
- `skills/sub-safety-screener.md` - Screen for coercion, abuse, stalking intent, minors, or manipulation requests; refuse harmful framing and surface support resources.
- `skills/sub-scoring-engine.md` - Score profile authenticity, communication health (Gottman markers), and compatibility signals against named frameworks.
- `skills/sub-improvement-roadmap.md` - Provide an authentic, respectful improvement plan for profile and communication with effort/impact ranking.

## Tools Required
- `WebSearch`, `WebFetch` - live evidence gathering
- `Read`, `Write` - artifact production
- `Bash`/`python` - run `tools/knowledge_updater.py`

## Knowledge Sources (crawl targets)
- PubMed / PsycINFO (relationship science)
- Semantic Scholar
- Crossref
- arXiv
- Journal of Social and Personal Relationships
- Gottman Institute research summaries

## Supporting Tools
- `tools/knowledge_updater.py` - API-based crawler that grows `SECOND-KNOWLEDGE-BRAIN.md` (weekly cron recommended).

## Active Development Tasks
- [x] Scaffold all required deliverables
- [x] Author main harness + 4 sub-skills with concrete I/O schemas
- [x] Define scoring dimensions: Authenticity, Communication health, Compatibility signal, Emotional safety, Clarity of intent
- [x] Seed and automate `SECOND-KNOWLEDGE-BRAIN.md`
- [x] Add 5+ regression scenarios and automated tests
- [x] Cross-skill cluster integration and scoring-scale alignment

## Related Root Docs
- `README.md` - quick start and safety note
- `PROJECT-detail.md` - full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` - phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` - living knowledge base
- `docs/cluster-integration.md` - cross-skill reuse contract
- `docs/adr/001-framework-and-scale.md` - architecture decision record
