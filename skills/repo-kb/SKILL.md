---
name: repo-kb
description: Use this skill when initializing, maintaining, querying, linting, or compiling a repository knowledge base that stores raw PR/review/incident/ADR/conversation notes and turns them into an LLM-maintained repo wiki. Also use it when periodically promoting durable lessons from that wiki into CLAUDE.md, REVIEW.md, .claude/rules, AGENTS.md, docs, or review guidance.
license: MIT
---

# Repo Knowledge Compiler

## Purpose

Maintain `.repo-kb/` as a persistent Markdown knowledge base for a software repository. It is an LLM wiki: raw operational logs go in first, then agents synthesize them into pages and review aspects, and only later promote stable lessons into project guidance or docs when the user asks for that maintenance.

Compilation creates reference outputs such as `.repo-kb/generated/claude-context.md`, `.repo-kb/generated/review.md`, and `.repo-kb/generated/rule-references/`. These outputs are inputs for a future LLM-guided update, not files to copy automatically into `CLAUDE.md`, `REVIEW.md`, `.claude/rules/`, `AGENTS.md`, or docs.

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
5. If `scripts/repo-kb` returns `permission denied` (common after `vendor` or a fresh clone when `core.fileMode=false`), run `chmod +x <skill-dir>/scripts/repo-kb` once before retrying.

## Operation Selection

Users do not need to know the Python helper path. Treat `/repo-kb <operation> ...`,
`repo-kb <operation> ...`, `$repo-kb ...`, and plain-language requests as user intent.
Choose the matching operation, then run the deterministic helper only when it is useful
for scaffolding, checks, collection, or workflow hints.

- **Initialize**: create `.repo-kb/` in a repository that does not have one yet.
- **Ingest**: add a PR, issue, review comment, incident note, ADR, chat/log excerpt, or human note into `.repo-kb/raw/`; synthesize into pages only when there is durable signal.
- **Ingest directory**: capture selected repository files into a *concatenated, per-file truncated* raw markdown snapshot (default `--max-bytes=20000` per file). Use this for external or point-in-time evidence. When you want to track the **live original** files in-repo without duplication, prefer the **In-Repo Reference Ingest (symlink)** pattern below.
- **Ingest PR comments**: collect GitHub PR review and conversation comments for a date range, then store them as raw review-comment evidence before synthesis.
- **Synthesize**: read recent raw notes and turn the repeatable signal into pages or review aspects. This is an LLM step; the helper only prints the workflow.
- **Query**: answer from `.repo-kb/index.md` and relevant pages, citing local paths.
- **Lint**: check frontmatter, links, sources, generated drift, page size, and stale claims.
- **Compile**: regenerate concise outputs from `.repo-kb/`.
- **Promote**: during explicit weekly/monthly maintenance, consult `.repo-kb/` and generated references, then intentionally update `CLAUDE.md`, rules, or docs.
- **Review PR**: read the diff and only the relevant review aspects, then review with repo-specific criteria.

Use `references/operations.md` for detailed workflows and `references/schema.md` for page contracts.

## CLI Helpers

The bundled script provides deterministic scaffolding and structural checks:

```bash
<installed-skill-dir>/scripts/repo-kb init
<installed-skill-dir>/scripts/repo-kb vendor
<installed-skill-dir>/scripts/repo-kb ingest --kind human-note --title "Title" --note "Sanitized note"
<installed-skill-dir>/scripts/repo-kb ingest-directory --path docs/adr --glob "*.md" --kind adr
<installed-skill-dir>/scripts/repo-kb ingest-pr-comments --since 2026-05-01 --until 2026-05-07
<installed-skill-dir>/scripts/repo-kb synthesize "since 2026-05-01"
<installed-skill-dir>/scripts/repo-kb lint
<installed-skill-dir>/scripts/repo-kb compile
<installed-skill-dir>/scripts/repo-kb compile --check
<installed-skill-dir>/scripts/repo-kb ask "Question"
<installed-skill-dir>/scripts/repo-kb promote --target CLAUDE.md --target REVIEW.md
<installed-skill-dir>/scripts/repo-kb operations
```

The repo-local wrapper hides the Python entrypoint when the skill is vendored:

```bash
.agents/skills/repo-kb/scripts/repo-kb ingest --kind human-note --title "Title" --note "Sanitized note"
.agents/skills/repo-kb/scripts/repo-kb ask "What should I know before touching src/api?"
.agents/skills/repo-kb/scripts/repo-kb promote --target CLAUDE.md --target REVIEW.md
```

For interactive agent usage, prefer user-facing intent:

```text
/repo-kb ingest DBトランザクション境界の教訓: 外部API呼び出しを中に入れない
/repo-kb synthesize 直近1週間の raw を pages / review-aspects に反映して
/repo-kb ask DBトランザクション境界の注意点は？
/repo-kb promote 今月の安定した知識だけ CLAUDE.md / REVIEW.md / rules に反映して
```

`synthesize`, `ask`, and `promote` are LLM-driven; the helper only prints the workflow and starting references. The agent reads the printed steps, opens the listed files, and edits `.repo-kb/` directly.

When installed through `gh skill`, treat the GitHub repository as the update source. It is acceptable to copy the skill into each target repository as a vendored repo-local skill.

Recommended target-repo layout:

```text
.agents/skills/repo-kb/      # neutral / multi-agent layout
# or
.claude/skills/repo-kb/      # Claude Code project-local skill
.repo-kb/                    # the knowledge base itself
```

Use `vendor` from the installed skill to create or refresh the repo-local copy:

```bash
<installed-skill-dir>/scripts/repo-kb vendor --path .agents/skills/repo-kb
<installed-skill-dir>/scripts/repo-kb vendor --path .agents/skills/repo-kb --force
```

After vendoring, repository-local automation can use:

```bash
.agents/skills/repo-kb/scripts/repo-kb ingest-directory --path docs/adr --glob "*.md" --kind adr
.agents/skills/repo-kb/scripts/repo-kb ingest-pr-comments --since 2026-05-01 --until 2026-05-07 --repo OWNER/REPO
.agents/skills/repo-kb/scripts/repo-kb lint
.agents/skills/repo-kb/scripts/repo-kb compile --check
.agents/skills/repo-kb/scripts/repo-kb ask "Question"
.agents/skills/repo-kb/scripts/repo-kb promote --target CLAUDE.md
```

Update flow: run `gh skill update` to refresh the installed source, then run `vendor --force` in each target repository that keeps a checked-in copy.

## Output Rules

Keep compiled files short and operational:

- `.repo-kb/generated/claude-context.md`: reference material for updating `CLAUDE.md`, `AGENTS.md`, or other agent instructions.
- `.repo-kb/generated/review.md`: reference material for updating `REVIEW.md` or review-only guidance.
- `.repo-kb/generated/rule-references/*.md`: reference material for updating `.claude/rules/` or other agent rule files.
- `.repo-kb/generated/*`: intermediate compiled outputs and summaries.

Do not create, overwrite, or auto-populate `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or other agent instruction files during init, ingest, lint, or compile. Let the LLM update those project files intentionally during a separate promotion task by consulting `.repo-kb/index.md`, relevant `.repo-kb/raw/` notes, pages, and `.repo-kb/generated/`.

Avoid turning `CLAUDE.md` into the wiki. If a project has one, it should point to `.repo-kb/` and include only high-signal rules needed at session start.

## In-Repo Reference Ingest (symlink pattern)

Use this pattern when the source of truth already lives in the repo (`docs/`, `.claude/skills/`, `.github/instructions/`, `.claude/rules/`, etc.) and you want `.repo-kb/` to reference rather than copy it.

Steps:

1. Create a category directory under `raw/` (e.g. `raw/docs/`, `raw/skills/`, `raw/copilot/`). Categories outside the standard `RAW_DIRS` (`pr/issues/incidents/adr/review-comments/logs/human-notes`) are allowed for symlink-based reference, since `ingest --kind ...` is not used for them.
2. Create relative symlinks pointing to the in-repo source:

   ```bash
   ln -s ../../docs raw/docs
   ln -s ../../../.claude/skills/code-review raw/skills/code-review
   ```

3. Add an index page under `pages/references/<topic>-index.md` listing the linked files via `../../raw/<category>/...` paths.
4. Document the deviation in `.repo-kb/SCHEMA.md` under a **Local Deviations** section (path, purpose, dependent index page).
5. Run `lint` and `compile --check` to confirm.

Why this is safe:

- pathlib `rglob` does **not** descend through directory symlinks, so lint never scans the symlink target's contents and never reports false-positive broken links from `.repo-kb`.
- Page link existence checks (`(path.parent / link).resolve()`) **do** follow symlinks, so broken references from index pages are still detected.
- Git stores symlinks as `mode 120000`, surviving clones (warn Windows users about `core.symlinks`).

When to choose which:

| Source                                                                        | Pattern                                              |
| ----------------------------------------------------------------------------- | ---------------------------------------------------- |
| External PR/issue/chat/incident, point-in-time snapshot                       | `ingest` / `ingest-directory` (copies content)       |
| In-repo `docs/`, skills, instructions, rules — kept as single source of truth | symlink                                              |
| Mixed: a long-lived doc you want quoted, but might diverge from upstream      | `ingest-directory` once, then keep reading from raw/ |

## Periodic Operation

Weekly routine arguments live in `.repo-kb/config.yaml` under the `weekly:` key so the agent does not have to invent them. The agent reads that section and executes the steps in order. Concretely:

1. For each entry in `weekly.ingest_directories`, run `ingest-directory --path <path> --glob <glob> --kind <kind>`. `kind` must be one of `pr | issue | incident | adr | review-comment | log | human-note`.
2. If `weekly.ingest_pr_comments.enabled` is true, compute `--since = today - window_days` and `--until = today`, then run `ingest-pr-comments --since ... --until ...`. Pass `--repo` only when `weekly.ingest_pr_comments.repo` is set; otherwise the script falls back to `gh repo view --json nameWithOwner`.
3. Run `synthesize` and act on its printed workflow: turn repeatable signal in recent raw notes into pages or review aspects. This is an LLM step; the helper does not write pages.
4. Run `lint`, then `compile`, then `compile --check` to confirm generated references converge.

Example (after the agent has read `config.yaml`):

```bash
.agents/skills/repo-kb/scripts/repo-kb ingest-directory --path docs/adr --glob "*.md" --kind adr
.agents/skills/repo-kb/scripts/repo-kb ingest-pr-comments --since 2026-05-04 --until 2026-05-11
.agents/skills/repo-kb/scripts/repo-kb synthesize "weekly 2026-05-04..2026-05-11"
.agents/skills/repo-kb/scripts/repo-kb lint
.agents/skills/repo-kb/scripts/repo-kb compile
.agents/skills/repo-kb/scripts/repo-kb compile --check
```

Use `operations` when the user asks how to run or automate repo-kb:

```bash
.agents/skills/repo-kb/scripts/repo-kb operations
```

For monthly or explicit promotion, consult `.repo-kb/index.md`, raw sources, pages, review aspects, and generated references, then open a focused PR for concise updates to `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or docs. Do not promote every raw note.

## Knowledge Governance

Strong claims need sources. A review aspect that can block or strongly influence a review should include at least one source entry unless the user explicitly marks it as a team policy.

If sources conflict, do not silently choose one. Record the conflict in `.repo-kb/reports/unresolved-contradictions.md` or the relevant page's `Open questions` section.

Mark aging knowledge with `last_verified`. Deprecate outdated rules instead of deleting them when historical context helps future maintainers.

## References

- `references/operations.md`: task workflows for init, ingest, query, lint, compile, and review.
- `references/schema.md`: recommended directory structure, frontmatter, and page anatomy.
- `assets/templates/`: starter `.repo-kb/` templates.
