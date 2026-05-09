# Repo KB Operations

## User-Facing Intent

Users should not need to remember the Python helper path. Interpret these forms as repo-kb intent:

```text
/repo-kb ingest DBトランザクション境界の教訓: 外部API呼び出しを中に入れない
/repo-kb ask DBトランザクション境界の注意点は？
/repo-kb promote 今月の安定した知識だけ CLAUDE.md / REVIEW.md / rules に反映して
```

Map the request to the relevant workflow, then run deterministic helpers only when useful. When a vendored skill exists, prefer the repo-local wrapper:

```bash
.agents/skills/repo-kb/scripts/repo-kb ingest --kind human-note --title "Transaction boundary review lesson" --note "Transactions must not wrap network I/O."
.agents/skills/repo-kb/scripts/repo-kb ask "What review aspects apply to src/api?"
.agents/skills/repo-kb/scripts/repo-kb promote --target CLAUDE.md --target REVIEW.md
```

## Initialize

1. Read existing repository guidance: `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, docs, ADRs, package files, and CI.
2. If the target repository should carry its own skill copy, vendor the skill into `.agents/skills/repo-kb/`.
3. Create `.repo-kb/` from templates if missing.
4. Do not create or overwrite `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or other agent instruction files automatically.
5. Seed `index.md` as a map of the wiki, not as mandatory project guidance.
6. Keep seeded pages and review aspects as drafts unless the user explicitly confirms they are active policy.
7. Compile reference outputs only for `.repo-kb/generated/`.
8. Ask before any separate promotion into project guidance files or docs.

Vendored setup:

```bash
<installed-skill-dir>/scripts/repo-kb vendor --path .agents/skills/repo-kb
.agents/skills/repo-kb/scripts/repo-kb init
```

## Ingest

1. Classify the source: `pr`, `issue`, `incident`, `adr`, `review-comment`, `log`, or `human-note`.
2. Save a sanitized raw note under `.repo-kb/raw/<kind>/`. Preserve enough original context that future agents can re-interpret it.
3. Extract tentative claims, decisions, review triggers, and anti-patterns into the raw note.
4. Update existing pages before creating new pages when the note contains durable signal.
5. Add source references in frontmatter or a `Sources` section whenever synthesis is updated.
6. Update `.repo-kb/index.md` and append `.repo-kb/log.md`.
7. Run lint and compile if generated reference outputs should change.

Use the helper for deterministic raw-source capture:

```bash
.agents/skills/repo-kb/scripts/repo-kb ingest \
  --kind human-note \
  --title "Transaction boundary review lesson" \
  --note "Transactions must not wrap network I/O."
```

Use period-based PR comment ingestion when the source is GitHub review or conversation feedback:

```bash
.agents/skills/repo-kb/scripts/repo-kb ingest-pr-comments \
  --since 2026-05-01 \
  --until 2026-05-07 \
  --repo OWNER/REPO
```

This requires the `gh` CLI. The command stores PR review comments and PR conversation comments in `.repo-kb/raw/review-comments/` as raw evidence. Use `--dry-run` to inspect the collected note before writing it. After ingestion, ask an agent to synthesize only durable, repeatable lessons into existing pages or draft review aspects.

Use directory ingestion for periodic repository paths such as ADRs, runbooks, support notes, or hand-maintained wiki exports:

```bash
.agents/skills/repo-kb/scripts/repo-kb ingest-directory \
  --path docs/adr \
  --glob "*.md" \
  --kind adr
```

The command captures matching files into one raw source. Keep the source path narrow enough that future agents can understand why the snapshot was ingested.

To create a draft review aspect while ingesting:

```bash
.agents/skills/repo-kb/scripts/repo-kb ingest \
  --kind review-comment \
  --title "Transaction boundary" \
  --note "Do not call external APIs inside DB transactions." \
  --as-review-aspect \
  --applies-to "src/api/**" \
  --review-question "Is there network I/O inside a DB transaction?"
```

The generated review aspect starts as `draft`. Promote it to `active` only after a human or agent has filled in trigger, good example, bad example, and source context.

## Query

1. Read `.repo-kb/index.md` first.
2. Open only pages relevant to the question.
3. Answer with local citations to `.repo-kb` pages or raw source paths.
4. If the answer creates durable knowledge, propose saving it as a page or note.

Use the helper when you want the deterministic workflow and starting references printed:

```bash
.agents/skills/repo-kb/scripts/repo-kb ask "What should I know before changing src/api?"
```

## Lint

Run deterministic lint first, then semantic review if needed.

Check:

- required files exist
- known frontmatter fields are present
- source references exist for review aspects
- generated files match compile output
- links point to existing local files
- pages are not overloaded with unrelated topics
- stale `last_verified` dates are visible
- contradictions are recorded instead of hidden

## Compile

1. Read `.repo-kb/config.yaml`.
2. Compile active conventions into `.repo-kb/generated/claude-context.md`.
3. Compile active review aspects into `.repo-kb/generated/review.md`.
4. Compile path-scoped rule references into `.repo-kb/generated/rule-references/*.md` when applicable.
5. Do not write `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or other agent instruction files; use generated files as references for intentional LLM edits.
6. Keep generated files reproducible. Manual edits belong in `.repo-kb/`.

## Promote To Project Guidance

Use this only when the user asks for periodic maintenance, such as a weekly or monthly repo knowledge review.

1. Read `.repo-kb/index.md`, relevant raw sources, pages, review aspects, and generated references.
2. Identify stable lessons that should affect future agents or human maintainers.
3. Ask before changing `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or docs if the requested scope is ambiguous.
4. Keep promoted guidance concise and link back to `.repo-kb/` for background.
5. Leave unresolved or low-confidence lessons in `.repo-kb/` rather than promoting them.

Use the helper when you want the deterministic promotion checklist and starting references printed:

```bash
.agents/skills/repo-kb/scripts/repo-kb promote --target CLAUDE.md --target REVIEW.md --target .claude/rules
```

## Periodic Maintenance

Weekly maintenance should grow `.repo-kb/`, not project guidance files directly:

1. Ingest selected directory notes, incident summaries, or sanitized session logs with `ingest --file` or `ingest-directory`.
2. Ingest PR comments for the target period with `ingest-pr-comments --since YYYY-MM-DD --until YYYY-MM-DD`.
3. Synthesize repeatable lessons into existing pages and review aspects. Keep uncertain items in raw notes or `Open Questions`.
4. Run `lint`, `compile`, and `compile --check`.
5. Commit `.repo-kb/` and generated reference changes together when they are intentional.

Monthly or explicit promotion should update project guidance by PR:

1. Read `.repo-kb/index.md`, active pages, active review aspects, and generated references.
2. Compare them with current `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, and docs.
3. Promote only stable, high-signal guidance needed at session start or review time.
4. Keep the PR small and link back to `.repo-kb/` for detailed background.

Use the helper's operations summary when a user asks how to operate the system:

```bash
.agents/skills/repo-kb/scripts/repo-kb operations
```

## Review PR

1. Inspect the diff and changed file paths.
2. Read `.repo-kb/index.md`.
3. Select review aspects whose `applies_to` patterns match changed paths.
4. Review against the selected aspects plus normal correctness, security, tests, and regression risk.
5. Report only actionable findings. If a new repeatable review lesson appears, propose ingesting it.
