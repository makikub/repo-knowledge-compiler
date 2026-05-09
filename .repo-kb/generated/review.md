# Review Guidance

This file is generated from `.repo-kb/review-aspects/`. Update review aspects, then run compile.

## High-Priority Checks

### Knowledge promotion drift
Severity: `medium`
Applies to: `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/**`, `docs/**`, `.repo-kb/**`

- Did the update consult relevant `.repo-kb/raw/` notes, pages, and generated references?
- Is the promoted guidance concise enough for startup context?
- Are low-confidence or unresolved lessons left in `.repo-kb/` instead of being promoted?
- Does `repo-kb compile --check` pass when generated references are expected to change?
Source: `.repo-kb/review-aspects/correctness/knowledge-promotion-drift.md`
