---
type: raw-source
kind: human-note
id: 2026-05-09-agent-rule-files-llm-maintained
date: 2026-05-09
source_ref: user-provided
---

# Agent rule files are LLM-maintained

## Original or Sanitized Note

Decision: repo-kb must not create or overwrite .claude/rules/ or other agent rule files automatically. These files are runtime agent instructions like CLAUDE.md, AGENTS.md, and REVIEW.md. repo-kb compile should instead write rule reference material under .repo-kb/generated/rules/. Users can then ask an LLM to consult repo-kb and intentionally create or update .claude/rules/ or equivalent agent rule files. This avoids damaging existing local rule policy while preserving a clear source path from repo-kb review aspects to proposed rules.

## Extracted Claims

- TODO: Extract durable claims, decisions, review triggers, and open questions.

## Integration Notes

- TODO: Link this source from related `.repo-kb/pages/` or `.repo-kb/review-aspects/`.
