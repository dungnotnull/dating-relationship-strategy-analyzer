# Contributing to Dating Profile & Relationship Strategy Analyzer

Thank you for considering a contribution. This project is a safety-sensitive,
research-first Claude skill, so we hold contributions to a high standard.

## How to contribute

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-change`.
3. Make your changes.
4. Run the full test suite: `python -m pytest tests/ -v`.
5. Commit with a clear message.
6. Open a pull request against `main`.

## Contribution guidelines

- **Framework-first:** every new scoring criterion or recommendation must cite a named, citable framework (Attachment Theory, Gottman Method, Sternberg, NVC, Self-Determination Theory, or Big Five compatibility research).
- **Safety-first:** any change to the safety gate must preserve or improve blocking of coercion, abuse, minors, stalking, and manipulation.
- **No placeholders:** do not submit TODOs, dummy code, or commented-out logic.
- **Tests required:** add or update tests for any functional change.
- **No live API runs in CI:** keep live crawls opt-in via `--dry-run` or explicit API keys.

## Code of conduct

Be respectful, evidence-based, and inclusive. Harassment or pseudoscientific claims will not be tolerated.

## Questions?

Open an issue with the `question` label.
