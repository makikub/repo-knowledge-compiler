# Review Guidance

This file is generated from `.repo-kb/review-aspects/`. Update review aspects, then run compile.

## High-Priority Checks

### Generated guidance drift
Severity: `medium`
Applies to: `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/generated/**`, `.repo-kb/**`

- Was the source knowledge updated before the generated guidance?
- Does `repo-kb compile --check` pass?
- Are review aspects backed by sources or explicitly marked as team policy?
Source: `.repo-kb/review-aspects/correctness/generated-guidance-drift.md`
