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
  - ".claude/rules/**"
  - ".repo-kb/**"
sources:
  - kind: human-note
    id: bootstrap
last_verified: bootstrap
---

# Generated guidance drift

## Why this matters

If generated reference guidance is stale after `.repo-kb/` changes, future agents may follow outdated or contradictory instructions. `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, and other agent instruction files are intentionally maintained by LLM edits, but those edits should still be traceable to `.repo-kb/`.

## Review trigger

- `.repo-kb/` changes
- `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or other agent instruction files change

## Review questions

- Was the source knowledge updated before generated references or project guidance changed?
- Does `repo-kb compile --check` pass for `.repo-kb/generated/`?
- Are review aspects backed by sources or explicitly marked as team policy?
- If agent instruction files changed, does the diff clearly follow `.repo-kb/index.md` or `.repo-kb/generated/`?

## Good example

Update `.repo-kb/review-aspects/`, compile `.repo-kb/generated/review.md`, then intentionally update `REVIEW.md` if needed.

## Bad example

Manually add a large new rule directly to `REVIEW.md` without updating or consulting `.repo-kb/`.
