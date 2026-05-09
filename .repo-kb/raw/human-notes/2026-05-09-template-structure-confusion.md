---
type: raw-source
kind: human-note
id: 2026-05-09-template-structure-confusion
date: 2026-05-09
source_ref: user-provided
---

# Template structure confusion

## Original or Sanitized Note

Dogfooding feedback: users still see template-structure drift. Even after project guidance files stopped being auto-written, hidden empty .claude/rules/generated directories can remain in local worktrees after deleting tracked .gitkeep files, and vendoring from that local filesystem can copy them into the skill package. Also, .repo-kb/generated/rules can read like actual agent rules rather than rule reference material. The skill should avoid packaging .claude templates and should name generated rule candidates as references, not rules.

## Extracted Claims

- TODO: Extract tentative claims, decisions, review triggers, and open questions.

## Integration Notes

- TODO: Link this source from related `.repo-kb/pages/` or `.repo-kb/review-aspects/`.
