---
type: knowledge-page
id: initial-repository-workflow
title: Initial repository workflow
status: draft
sources:
  - kind: human-note
    id: 2026-05-09-repo-kb-as-raw-log-wiki
    path: .repo-kb/raw/human-notes/2026-05-09-repo-kb-as-raw-log-wiki.md
last_verified: 2026-05-09
---

# Initial repository workflow

## Summary

Use `.repo-kb/` as the durable LLM wiki for repository memory. Put raw PR notes, review comments, incidents, design discussions, debugging logs, and human notes here first; promote only stable lessons into project guidance or docs during explicit maintenance.

## Current Practice

- Add raw evidence to `.repo-kb/raw/` when it is safe to store.
- Synthesize durable patterns into `.repo-kb/pages/` or `.repo-kb/review-aspects/`.
- Compile `.repo-kb/generated/` as reference material.
- Update `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or docs only during an explicit promotion task.

## Rationale

Agent context files stay useful when they are concise. The larger knowledge base can preserve messy history and raw context while promoted guidance remains targeted.

## Related Pages

- [Knowledge promotion drift](../../review-aspects/correctness/knowledge-promotion-drift.md)

## Open Questions

- Which existing repository documents or logs should be ingested first?
- What cadence should this repository use for promoting stable lessons into guidance or docs?
