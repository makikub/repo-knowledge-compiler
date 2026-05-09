---
type: knowledge-page
id: project-guidance-files
title: Project guidance files
status: active
sources:
  - kind: human-note
    id: 2026-05-09-project-guidance-files-llm-maintained
    path: .repo-kb/raw/human-notes/2026-05-09-project-guidance-files-llm-maintained.md
  - kind: human-note
    id: 2026-05-09-agent-rule-files-llm-maintained
    path: .repo-kb/raw/human-notes/2026-05-09-agent-rule-files-llm-maintained.md
  - kind: human-note
    id: 2026-05-09-repo-kb-as-raw-log-wiki
    path: .repo-kb/raw/human-notes/2026-05-09-repo-kb-as-raw-log-wiki.md
  - kind: human-note
    id: 2026-05-09-template-structure-confusion
    path: .repo-kb/raw/human-notes/2026-05-09-template-structure-confusion.md
last_verified: 2026-05-09
---

# Project guidance files

## Summary

`repo-kb init` must not create `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or other agent instruction files, and `repo-kb compile` must not overwrite or auto-populate them. These files belong to each repository and should be updated intentionally by an LLM or human after consulting `.repo-kb/`, usually during explicit weekly/monthly maintenance or a user-requested promotion task.

## Current Practice

- `init` creates `.repo-kb/` only.
- `compile` writes `.repo-kb/generated/claude-context.md`, `.repo-kb/generated/review.md`, and `.repo-kb/generated/rule-references/`.
- `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, and other agent instruction files are manually or LLM-maintained project files.
- When those files need updates, consult `.repo-kb/index.md`, relevant `.repo-kb/raw/` notes, pages, and `.repo-kb/generated/`.
- Do not distribute agent instruction files as init templates.
- Do not copy every generated reference into `.claude/rules/`; promote only stable, high-signal lessons.
- Do not keep `.claude/` under `assets/templates/`; even unused empty template directories make init behavior ambiguous.
- Name compiled rule candidates as `rule-references` so they are not confused with runnable agent rules.

## Rationale

Target repositories often already have project guidance and rule files with local policy. Creating, overwriting, or auto-populating them during `init` risks damaging existing instructions. Generated reference files are enough for an agent to understand what may be worth reflecting, while leaving the final edit to an intentional LLM action.

## Related Pages

- [Initial repository workflow](initial-repository-workflow.md)
- [Repo Knowledge Compiler concept](../architecture/repo-knowledge-compiler-concept.md)

## Open Questions

- Should `compile` eventually offer an explicit opt-in flag that writes proposed patches for project guidance or rule files?
