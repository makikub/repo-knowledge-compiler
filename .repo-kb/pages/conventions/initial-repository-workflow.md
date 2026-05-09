---
type: knowledge-page
id: initial-repository-workflow
title: Initial repository workflow
status: active
sources:
  - kind: human-note
    id: bootstrap
last_verified: bootstrap
---

# Initial repository workflow

## Summary

Use `.repo-kb/` as the durable source for repository conventions, review aspects, design decisions, and operational lessons. Compile concise outputs from it instead of manually expanding agent instruction files.

## Current Practice

- Add durable knowledge to `.repo-kb/pages/` or `.repo-kb/review-aspects/`.
- Keep raw evidence in `.repo-kb/raw/` when it is safe to store.
- Regenerate `REVIEW.md` and `.repo-kb/generated/` after knowledge changes.

## Rationale

Agent context files stay useful when they are concise. The larger knowledge base can grow in Markdown while compiled outputs remain targeted.

## Related Pages

- [Generated guidance drift](../../review-aspects/correctness/generated-guidance-drift.md)

## Open Questions

- Which existing repository documents should be ingested first?
