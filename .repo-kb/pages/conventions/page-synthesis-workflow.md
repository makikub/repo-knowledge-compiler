---
type: knowledge-page
id: page-synthesis-workflow
title: Page synthesis is a manual LLM step
status: active
sources:
  - kind: human-note
    id: 2026-05-11-page-synthesis-trigger
    path: .repo-kb/raw/human-notes/2026-05-11-page-synthesis-trigger.md
last_verified: 2026-05-11
---

# Page synthesis is a manual LLM step

## Summary

`pages/` and `review-aspects/` are never created automatically. None of `ingest`, `ingest-directory`, `ingest-pr-comments`, `lint`, or `compile` write into `pages/` or `review-aspects/`. Synthesis from raw notes into durable pages is an explicit LLM-judgment step that the operator must run after ingest.

## Current Practice

- `ingest*` commands only land sanitized evidence under `.repo-kb/raw/`.
- `compile` aggregates pages and review aspects that are already `status: active`. It does not promote raw notes.
- After every ingest, the LLM must decide whether the new raw note contains durable signal and update existing pages before creating new ones.
- Trigger for new page creation: a theme appears across **3 or more raw notes / ingested documents**, or the theme is already covered by an existing page that needs updating.
- A symlink-pattern index page under `pages/references/<topic>-index.md` is a navigation aid, not a synthesis. Creating an index page does not complete the ingest workflow.

## Rationale

Automating page creation produces noisy, low-signal pages that pollute the knowledge base and dilute the value of `.repo-kb/generated/`. Leaving synthesis as a deliberate LLM step preserves the wiki's signal-to-noise ratio at the cost of requiring a final judgment call.

The recently observed failure mode: a session ingested `docs/` via the symlink pattern, created a `pages/references/...-index.md`, and stopped. Cross-cutting lessons present across multiple docs were not promoted to `pages/conventions/...` or `review-aspects/...`. The index existed; the synthesis did not.

## Related Pages

- [Initial repository workflow](./initial-repository-workflow.md)
- [Knowledge promotion drift](../../review-aspects/correctness/knowledge-promotion-drift.md)

## Open Questions

- Should the helper print a synthesis-reminder banner after `ingest*` commands?
- What is the right cadence for re-checking older raw notes for cross-cutting themes that only become visible after later ingests?
