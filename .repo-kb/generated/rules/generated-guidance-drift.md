---
paths:
  - "CLAUDE.md"
  - "AGENTS.md"
  - "REVIEW.md"
  - ".claude/rules/**"
  - ".repo-kb/**"
---

# Generated guidance drift

Reference generated from `.repo-kb/review-aspects/`. If this should become an agent rule, ask an LLM to intentionally update the project rule file.

- Was the source knowledge updated before generated references or project guidance changed?
- Does `repo-kb compile --check` pass for `.repo-kb/generated/`?
- Are review aspects backed by sources or explicitly marked as team policy?
- If agent instruction files changed, does the diff clearly follow `.repo-kb/index.md` or `.repo-kb/generated/`?
