# Review Guidance

This file is generated from `.repo-kb/review-aspects/`. Update review aspects, then run compile.

## High-Priority Checks

### Generated guidance drift
Severity: `medium`
Applies to: `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/**`, `.repo-kb/**`

- Was the source knowledge updated before generated references or project guidance changed?
- Does `repo-kb compile --check` pass for `.repo-kb/generated/`?
- Are review aspects backed by sources or explicitly marked as team policy?
- If agent instruction files changed, does the diff clearly follow `.repo-kb/index.md` or `.repo-kb/generated/`?
Source: `.repo-kb/review-aspects/correctness/generated-guidance-drift.md`
