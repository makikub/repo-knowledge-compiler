---
type: review-aspect
id: knowledge-promotion-drift
title: Knowledge promotion drift
severity: medium
status: active
applies_to:
  - "CLAUDE.md"
  - "AGENTS.md"
  - "REVIEW.md"
  - ".claude/rules/**"
  - "docs/**"
  - ".repo-kb/**"
sources:
  - kind: human-note
    id: 2026-05-09-repo-kb-as-raw-log-wiki
    path: .repo-kb/raw/human-notes/2026-05-09-repo-kb-as-raw-log-wiki.md
last_verified: 2026-05-09
---

# Knowledge promotion drift

## Why this matters

`.repo-kb/` is the raw log and LLM wiki. `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, and docs should contain only stable lessons intentionally promoted from that wiki. Promotion should be traceable to raw sources, pages, or generated references.

## Review trigger

- A maintenance task promotes `.repo-kb/` knowledge into project guidance or docs.
- `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or docs change because of repo knowledge.

## Review questions

- Did the update consult relevant `.repo-kb/raw/` notes, pages, and generated references?
- Is the promoted guidance concise enough for startup context?
- Are low-confidence or unresolved lessons left in `.repo-kb/` instead of being promoted?
- Does `repo-kb compile --check` pass when generated references are expected to change?

## Good example

During monthly maintenance, read `.repo-kb/index.md`, relevant raw notes, and `.repo-kb/generated/`, then add one concise rule to `CLAUDE.md` with a link back to the source page.

## Bad example

During init, create `.claude/rules/generated/` and copy every generated reference into it as mandatory agent guidance.
