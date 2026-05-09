---
type: raw-source
kind: human-note
id: 2026-05-09-project-guidance-files-llm-maintained
date: 2026-05-09
source_ref: user-provided
---

# Project guidance files are LLM-maintained

## Original or Sanitized Note

Decision: repo-kb init must not create CLAUDE.md, AGENTS.md, or REVIEW.md. Existing target repositories may already have those files and automatic creation or replacement risks overwriting local policy. repo-kb compile should generate reference material under .repo-kb/generated/ and generated rules, but top-level project guidance files should be updated intentionally by the LLM after consulting .repo-kb/index.md, .repo-kb/generated/claude-context.md, and .repo-kb/generated/review.md. This keeps .repo-kb as the durable source of truth while preserving local ownership of agent instruction files. Templates for CLAUDE.md and REVIEW.md should not be distributed as init outputs.

## Extracted Claims

- TODO: Extract durable claims, decisions, review triggers, and open questions.

## Integration Notes

- TODO: Link this source from related `.repo-kb/pages/` or `.repo-kb/review-aspects/`.
