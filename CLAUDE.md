# Project Instructions

This repository uses `.repo-kb/` as the raw log and LLM wiki for durable repo knowledge.
This file is manually maintained by consulting `.repo-kb/index.md` and `.repo-kb/generated/claude-context.md`.

## Always Follow

- Before substantial work, check `.repo-kb/index.md` and relevant `.repo-kb/pages/`.
- During code review, use `REVIEW.md`, `.repo-kb/generated/review.md`, and relevant `.repo-kb/review-aspects/`.
- Propose new `.repo-kb/raw/` entries for repeated review findings, incidents, design discussions, debugging logs, and important repo-specific practices.
- Do not assume `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, or `.claude/rules/` are generated. Update `.repo-kb/`, run compile, then intentionally promote concise guidance only if needed.

## Generated Context

See `.repo-kb/generated/claude-context.md`.
