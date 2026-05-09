---
name: repo-kb
description: Use this skill when initializing, maintaining, querying, linting, or compiling a repository knowledge base that stores raw PR/review/incident/ADR/conversation notes and turns them into an LLM-maintained repo wiki. Also use it when periodically promoting durable lessons from that wiki into CLAUDE.md, REVIEW.md, .claude/rules, AGENTS.md, docs, or review guidance.
license: MIT
---

# Repo Knowledge Compiler

## Purpose

Maintain `.repo-kb/` as a persistent Markdown knowledge base for a software repository. It is an LLM wiki: raw operational logs go in first, then agents synthesize them into pages and review aspects, and only later promote stable lessons into project guidance or docs when the user asks for that maintenance.

Compilation creates reference outputs such as `.repo-kb/generated/claude-context.md`, `.repo-kb/generated/review.md`, and `.repo-kb/generated/rules/`. These outputs are inputs for a future LLM-guided update, not files to copy automatically into `CLAUDE.md`, `REVIEW.md`, `.claude/rules/`, `AGENTS.md`, or docs.

The core pattern is:

- raw sources are the primary evidence and may contain the messy original context
- knowledge pages are LLM-maintained synthesis over those raw sources
- generated outputs are deterministic reference material for later promotion
- project guidance files and docs are updated intentionally during weekly/monthly or user-requested maintenance

## First Checks

Before editing a target repository:

1. Inspect existing `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, ADRs, docs, and package/CI files.
2. If the task is review or bug-fix related, check recent history for affected files with `git log --oneline -- <file>`.
3. Do not rewrite large generated outputs directly. Update `.repo-kb/` first, then compile.
4. Treat secrets, customer data, private chat logs, and personal data as unsafe raw sources unless the user explicitly provides sanitized notes.

## Operation Selection

- **Initialize**: create `.repo-kb/` in a repository that does not have one yet.
- **Ingest**: add a PR, issue, review comment, incident note, ADR, chat/log excerpt, or human note into `.repo-kb/raw/`; synthesize into pages only when there is durable signal.
- **Query**: answer from `.repo-kb/index.md` and relevant pages, citing local paths.
- **Lint**: check frontmatter, links, sources, generated drift, page size, and stale claims.
- **Compile**: regenerate concise outputs from `.repo-kb/`.
- **Promote**: during explicit weekly/monthly maintenance, consult `.repo-kb/` and generated references, then intentionally update `CLAUDE.md`, rules, or docs.
- **Review PR**: read the diff and only the relevant review aspects, then review with repo-specific criteria.

Use `references/operations.md` for detailed workflows and `references/schema.md` for page contracts.

## CLI Helpers

The bundled script provides deterministic scaffolding and structural checks:

```bash
python3 <installed-skill-dir>/scripts/repo_kb.py init
python3 <installed-skill-dir>/scripts/repo_kb.py vendor
python3 <installed-skill-dir>/scripts/repo_kb.py ingest --kind human-note --title "Title" --note "Sanitized note"
python3 <installed-skill-dir>/scripts/repo_kb.py lint
python3 <installed-skill-dir>/scripts/repo_kb.py compile
python3 <installed-skill-dir>/scripts/repo_kb.py compile --check
```

When installed through `gh skill`, treat the GitHub repository as the update source. It is acceptable to copy the skill into each target repository as a vendored repo-local skill.

Recommended target-repo layout:

```text
.agents/skills/repo-kb/
.repo-kb/
```

Use `vendor` from the installed skill to create or refresh the repo-local copy:

```bash
python3 <installed-skill-dir>/scripts/repo_kb.py vendor --path .agents/skills/repo-kb
python3 <installed-skill-dir>/scripts/repo_kb.py vendor --path .agents/skills/repo-kb --force
```

After vendoring, repository-local automation can use:

```bash
python3 .agents/skills/repo-kb/scripts/repo_kb.py lint
python3 .agents/skills/repo-kb/scripts/repo_kb.py compile --check
```

Update flow: run `gh skill update` to refresh the installed source, then run `vendor --force` in each target repository that keeps a checked-in copy.

## Output Rules

Keep compiled files short and operational:

- `.repo-kb/generated/claude-context.md`: reference material for updating `CLAUDE.md`, `AGENTS.md`, or other agent instructions.
- `.repo-kb/generated/review.md`: reference material for updating `REVIEW.md` or review-only guidance.
- `.repo-kb/generated/rules/*.md`: reference material for updating `.claude/rules/` or other agent rule files.
- `.repo-kb/generated/*`: intermediate compiled outputs and summaries.

Do not create, overwrite, or auto-populate `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or other agent instruction files during init, ingest, lint, or compile. Let the LLM update those project files intentionally during a separate promotion task by consulting `.repo-kb/index.md`, relevant `.repo-kb/raw/` notes, pages, and `.repo-kb/generated/`.

Avoid turning `CLAUDE.md` into the wiki. If a project has one, it should point to `.repo-kb/` and include only high-signal rules needed at session start.

## Knowledge Governance

Strong claims need sources. A review aspect that can block or strongly influence a review should include at least one source entry unless the user explicitly marks it as a team policy.

If sources conflict, do not silently choose one. Record the conflict in `.repo-kb/reports/unresolved-contradictions.md` or the relevant page's `Open questions` section.

Mark aging knowledge with `last_verified`. Deprecate outdated rules instead of deleting them when historical context helps future maintainers.

## References

- `references/operations.md`: task workflows for init, ingest, query, lint, compile, and review.
- `references/schema.md`: recommended directory structure, frontmatter, and page anatomy.
- `assets/templates/`: starter `.repo-kb/` templates.
