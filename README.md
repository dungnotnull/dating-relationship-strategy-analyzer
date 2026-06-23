# 💞 Dating Profile & Relationship Strategy Analyzer

> An evidence-based, safety-first Claude skill that scores dating profiles and relationship communication against world-renowned psychology frameworks — and produces a prioritized improvement roadmap.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-40%20passed-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Open Source](https://img.shields.io/badge/open%20source-%E2%9D%A4-red.svg)](https://github.com/dungnotnull/dating-relationship-strategy-analyzer)

---

## 🌟 Why this exists

Most dating advice is opinion, manipulation, or "game." People deserve better: **relationship science** applied with empathy, transparency, and safety.

This skill turns Claude into a research-first relationship-science coach grounded in **attachment theory**, **the Gottman Method**, **Sternberg's Triangular Theory of Love**, **Nonviolent Communication**, **Self-Determination Theory**, and **Big Five compatibility research**.

It is part of the **Health, Wellness & Psychology** cluster.

---

## 🧠 What it does

```
User request
    ↓
[1] Profile Intake — structured inputs, masked identifiers
    ↓
[2] HARD Safety Gate — blocks coercion, abuse, minors, manipulation
    ↓
[3] Framework Selection — picks the right science for the case
    ↓
[4] Evidence Gathering — PubMed / Semantic Scholar / Crossref / arXiv
    ↓
[5] Scoring Engine — 0-100 across 5 dimensions
    ↓
[6] Improvement Roadmap — effort × impact prioritized actions
    ↓
[7] Devil's Advocate — challenges its own conclusions
    ↓
Professional artifact + citations
```

### The 5 scoring dimensions

| Dimension | Framework anchor | What it measures |
|---|---|---|
| **Authenticity** | Attachment Theory + Self-Determination Theory | Values-based, bounded self-presentation |
| **Communication Health** | Gottman Method + Nonviolent Communication | Absence of Four Horsemen, presence of repair |
| **Compatibility Signal** | Sternberg + Big Five compatibility | Values, goals, and intent alignment |
| **Emotional Safety** | Gottman safe-haven + Attachment safe-haven | Validation, consent, boundary respect |
| **Clarity of Intent** | NVC clear requests + explicit intent | Direct, mutual understanding |

Composite score = weighted mean with transparent, adjustable weights.

---

## 🚀 Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the test suite

```bash
python -m pytest tests/ -v
```

Expected: **40 passed**.

### 3. Refresh the knowledge base (dry run, no writes)

```bash
python tools/knowledge_updater.py --dry-run --since 2024-01-01 --max-results 5
```

For live crawling, optionally set an NCBI API key:

```bash
export NCBI_API_KEY="your_ncbi_key"
python tools/knowledge_updater.py --since 2024-01-01
```

### 4. Use the skill

Load `skills/main.md` into Claude. The harness will guide intake, run the safety gate, gather evidence, score, and build a roadmap.

---

## 📁 Repository layout

```
dating-relationship-strategy-analyzer/
├── skills/
│   ├── main.md                      # Main harness
│   ├── sub-profile-intake.md        # Structured intake stage
│   ├── sub-safety-screener.md       # HARD safety/risk gate
│   ├── sub-scoring-engine.md        # 5-dimension scorecard
│   └── sub-improvement-roadmap.md   # Effort × impact roadmap
├── tools/
│   └── knowledge_updater.py         # PubMed / Semantic Scholar / Crossref / arXiv crawler
├── tests/
│   ├── scenarios.json               # 8 validation scenarios
│   ├── test-scenarios.md            # Scenario documentation
│   ├── test_knowledge_updater.py    # Crawler unit tests
│   ├── test_scenarios.py            # Scenario contract tests
│   └── test_skills.py               # Skill structure tests
├── docs/
│   ├── cluster-integration.md       # Cross-skill reuse contract
│   └── adr/
│       └── 001-framework-and-scale.md # Architecture decision record
├── SECOND-KNOWLEDGE-BRAIN.md        # Living, citable knowledge base
├── PROJECT-detail.md                # Full technical specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md # Phase roadmap
├── CLAUDE.md                        # Skill identity and quick reference
├── requirements.txt
└── README.md
```

---

## 🛡️ Safety first

This skill will **refuse or refer** before producing any strategy if it detects:

- Manipulation, deception, gaslighting, or coercive control
- Stalking, surveillance, or non-consensual contact
- Minors in romantic/sexual contexts
- Imminent danger or severe abuse
- Catfishing or fake personas

Support resources are surfaced automatically, including the National Domestic Violence Hotline and Crisis Text Line.

---

## 📚 Knowledge base

`SECOND-KNOWLEDGE-BRAIN.md` is a living, self-updating literature base. It is seeded with foundational papers such as:

- Hazan & Shaver (1987) — adult attachment in romantic love
- Gottman & Levenson (1992) — Four Horsemen predict dissolution
- Sternberg (1986) — triangular theory of love
- Rosenberg (2003) — Nonviolent Communication
- Fraley & Shaver (2000) — adult attachment theory review
- Levine & Heller (2010) — attachment in modern dating

The crawler adds fresh papers weekly with de-duplication by DOI/URL hash.

---

## 🧪 Validation

Eight end-to-end scenarios cover the full harness:

1. Dating profile rewrite — authenticity-focused, no deception
2. Conflict text-thread analysis — Gottman + NVC repair
3. Manipulation request — refused
4. Possible abusive partner — referred to hotlines
5. Anxious attachment self-improvement — roadmap + therapy note
6. Minor safety — age-appropriate referral
7. Deceptive profile / catfishing — refused
8. Compatibility question — scored with cited research

---

## 🤝 Cluster integration

This skill belongs to the **Health, Wellness & Psychology** cluster. Its sub-skills, scoring scale, and safety gate are designed for reuse by sibling skills. See `docs/cluster-integration.md` for the reuse contract and `docs/adr/001-framework-and-scale.md` for design rationale.

---

## 🛠️ Tech stack

- Python 3.11+
- `httpx` for async HTTP crawling
- `pytest` + `pytest-asyncio` for testing
- Markdown skill files for Claude

---

## 📜 License

MIT — see [LICENSE](LICENSE).

---

## 🙋 Contributing

Contributions that improve evidence quality, safety, or accessibility are welcome. Please keep all judgments anchored to named, citable frameworks. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 🔭 Roadmap

- [x] Phase 0 — Research & Skill Architecture
- [x] Phase 1 — Core Sub-Skills
- [x] Phase 2 — Main Harness + Quality Gates
- [x] Phase 3 — SECOND-KNOWLEDGE-BRAIN Pipeline
- [x] Phase 4 — Testing & Validation
- [x] Phase 5 — Integration & Cross-Skill Wiring
- [ ] Live knowledge-base refresh in production
- [ ] Optional LangChain/LLM harness integration
- [ ] Multi-language safety resources

---

> *"Research-first, safety-first, always."*
