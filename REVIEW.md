# Review Guidance

This file is manually maintained by consulting `.repo-kb/generated/review.md` and `.repo-kb/review-aspects/`.

## High-Priority Checks

### Generated guidance drift
Severity: `medium`
Applies to: `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/**`, `.repo-kb/**`

- Was the source knowledge updated before the generated guidance?
- Does `repo-kb compile --check` pass for generated reference outputs?
- Are review aspects backed by sources or explicitly marked as team policy?
Source: `.repo-kb/review-aspects/correctness/generated-guidance-drift.md`
