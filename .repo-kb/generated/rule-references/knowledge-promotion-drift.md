---
paths:
  - "CLAUDE.md"
  - "AGENTS.md"
  - "REVIEW.md"
  - ".claude/rules/**"
  - "docs/**"
  - ".repo-kb/**"
---

# Knowledge promotion drift

Reference generated from `.repo-kb/review-aspects/`. If this should become an agent rule, ask an LLM to intentionally update the project rule file.

- Did the update consult relevant `.repo-kb/raw/` notes, pages, and generated references?
- Is the promoted guidance concise enough for startup context?
- Are low-confidence or unresolved lessons left in `.repo-kb/` instead of being promoted?
- Does `repo-kb compile --check` pass when generated references are expected to change?
