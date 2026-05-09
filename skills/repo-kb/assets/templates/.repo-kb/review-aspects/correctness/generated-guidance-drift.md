---
type: review-aspect
id: generated-guidance-drift
title: Generated guidance drift
severity: medium
status: active
applies_to:
  - "CLAUDE.md"
  - "AGENTS.md"
  - "REVIEW.md"
  - ".claude/rules/generated/**"
  - ".repo-kb/**"
sources:
  - kind: human-note
    id: bootstrap
last_verified: bootstrap
---

# Generated guidance drift

## Why this matters

If generated agent guidance is edited directly or not regenerated after `.repo-kb/` changes, future agents may follow stale or contradictory instructions.

## Review trigger

- `.repo-kb/` changes
- `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, or `.claude/rules/generated/` changes

## Review questions

- Was the source knowledge updated before the generated guidance?
- Does `repo-kb compile --check` pass?
- Are review aspects backed by sources or explicitly marked as team policy?

## Good example

Update `.repo-kb/review-aspects/`, then regenerate `REVIEW.md`.

## Bad example

Manually add a large new rule directly to `REVIEW.md` without updating `.repo-kb/`.
