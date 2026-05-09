# Repo KB Schema

## Directory Layout

```text
.repo-kb/
  SCHEMA.md
  config.yaml
  index.md
  log.md
  raw/
    pr/
    issues/
    incidents/
    adr/
    review-comments/
    logs/
    human-notes/
  pages/
    architecture/
    conventions/
    decisions/
    runbooks/
    anti-patterns/
    invariants/
  review-aspects/
    correctness/
    security/
    performance/
    testing/
    frontend/
    migration/
    observability/
  generated/
  reports/
```

## Knowledge Page

```markdown
---
type: knowledge-page
id: short-stable-id
title: Human Title
status: active
sources:
  - kind: human-note
    id: YYYY-MM-DD-topic
last_verified: YYYY-MM-DD
---

# Human Title

## Summary

## Current Practice

## Rationale

## Related Pages

## Open Questions
```

## Review Aspect

```markdown
---
type: review-aspect
id: transaction-boundary
title: DB transaction boundary
severity: high
status: active
applies_to:
  - "src/api/**"
sources:
  - kind: pr
    id: "PR-123"
last_verified: YYYY-MM-DD
---

# DB transaction boundary

## Why this matters

## Review trigger

## Review questions

## Good example

## Bad example
```

## Raw Source Note

```markdown
---
type: raw-source
kind: human-note
id: YYYY-MM-DD-topic
date: YYYY-MM-DD
source_ref: user-provided
---

# Source title

## Original or Sanitized Note

## Extracted Claims
```

Raw sources are the first landing place for operational memory: PR notes, review comments, incident timelines, ADRs, chat summaries, debugging logs, and human notes. They should preserve the original context in sanitized form. Knowledge pages and review aspects are later synthesis over raw sources; they are not required for every raw note.

## Status Values

- `active`: currently valid
- `draft`: not yet trusted for generated outputs
- `deprecated`: retained for history but not compiled

## Compile Policy

Only `active` knowledge pages and review aspects should affect generated outputs by default. Draft pages may be referenced manually but should not become mandatory review guidance.

Generated outputs under `.repo-kb/generated/` are reference material for later LLM-guided promotion. They are not automatically copied to `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or docs.
