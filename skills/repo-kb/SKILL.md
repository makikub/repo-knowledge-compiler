---
name: repo-kb
description: Use this skill when initializing, maintaining, querying, linting, or compiling a repository knowledge base that turns PRs, reviews, incidents, ADRs, conventions, and implicit team knowledge into CLAUDE.md, REVIEW.md, .claude/rules, AGENTS.md, or review guidance. Also use it when adapting Karpathy's LLM Wiki pattern to development repositories or when asked to grow repo-local AI instructions from operational knowledge.
license: MIT
---

# Repo Knowledge Compiler

## Purpose

Maintain `.repo-kb/` as a persistent Markdown knowledge base for a software repository, then compile the durable parts into concise reference outputs such as `.repo-kb/generated/claude-context.md`, `.repo-kb/generated/review.md`, and `.repo-kb/generated/rules/`.

The core pattern is:

- raw sources are immutable evidence
- knowledge pages are LLM-maintained synthesis
- generated outputs are deterministic projections
- humans review knowledge changes through normal repo review

## First Checks

Before editing a target repository:

1. Inspect existing `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, ADRs, docs, and package/CI files.
2. If the task is review or bug-fix related, check recent history for affected files with `git log --oneline -- <file>`.
3. Do not rewrite large generated outputs directly. Update `.repo-kb/` first, then compile.
4. Treat secrets, customer data, private chat logs, and personal data as unsafe raw sources unless the user explicitly provides sanitized notes.

## Operation Selection

- **Initialize**: create `.repo-kb/` in a repository that does not have one yet.
- **Ingest**: add a PR, issue, review comment, incident note, ADR, or human note into `.repo-kb/raw/` and integrate it into pages.
- **Query**: answer from `.repo-kb/index.md` and relevant pages, citing local paths.
- **Lint**: check frontmatter, links, sources, generated drift, page size, and stale claims.
- **Compile**: regenerate concise outputs from `.repo-kb/`.
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

Do not create or overwrite `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or other agent instruction files automatically. Let the LLM update those project files intentionally by consulting `.repo-kb/index.md` and `.repo-kb/generated/`.

Avoid turning `CLAUDE.md` into the wiki. If a project has one, it should point to `.repo-kb/` and include only high-signal rules needed at session start.

## Knowledge Governance

Strong claims need sources. A review aspect that can block or strongly influence a review should include at least one source entry unless the user explicitly marks it as a team policy.

If sources conflict, do not silently choose one. Record the conflict in `.repo-kb/reports/unresolved-contradictions.md` or the relevant page's `Open questions` section.

Mark aging knowledge with `last_verified`. Deprecate outdated rules instead of deleting them when historical context helps future maintainers.

## References

- `references/operations.md`: task workflows for init, ingest, query, lint, compile, and review.
- `references/schema.md`: recommended directory structure, frontmatter, and page anatomy.
- `assets/templates/`: starter `.repo-kb/` templates.
