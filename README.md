# Repo Knowledge Compiler

Repo Knowledge Compiler adapts Karpathy's LLM Wiki pattern to software repositories.

Instead of putting every project rule into `CLAUDE.md` or `AGENTS.md`, each target repository keeps operational memory in `.repo-kb/`:

- PR and review lessons
- incidents and bug patterns
- architecture decisions
- raw debugging logs and discussion notes
- conventions and invariants
- code-review aspects

Raw notes are the first landing place. Agents later synthesize durable patterns into wiki pages and review aspects, then compile concise reference outputs such as `.repo-kb/generated/claude-context.md`, `.repo-kb/generated/review.md`, and `.repo-kb/generated/rule-references/`.

Those generated files are reference material for a later promotion task. `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, and docs should be updated intentionally, for example during weekly or monthly repo-knowledge maintenance.

## Repository Shape

```text
.codex-plugin/plugin.json
skills/
  repo-kb/
    SKILL.md
    references/
    scripts/repo_kb.py
    assets/templates/
```

## Install With gh skill

`gh skill` is part of GitHub CLI and is currently in public preview. Use GitHub CLI 2.90.0 or later.

```bash
gh --version
gh skill --help
```

Always preview a skill before installing it:

```bash
gh skill preview makikub/repo-knowledge-compiler repo-kb
```

Install into the current repository for Claude Code:

```bash
cd /path/to/target-repo
gh skill install makikub/repo-knowledge-compiler repo-kb --agent claude-code --scope project
```

Install for all of your Claude Code projects:

```bash
gh skill install makikub/repo-knowledge-compiler repo-kb --agent claude-code --scope user
```

Install into the current repository for Codex:

```bash
cd /path/to/target-repo
gh skill install makikub/repo-knowledge-compiler repo-kb --agent codex --scope project
```

Pin to a tag or commit SHA when you want reproducible installs:

```bash
gh skill install makikub/repo-knowledge-compiler repo-kb --agent claude-code --scope project --pin v0.1.0
gh skill install makikub/repo-knowledge-compiler repo-kb@v0.1.0 --agent claude-code --scope project
```

Use either `--pin` or `skill@version`, not both.

Update installed skills:

```bash
gh skill update
gh skill update repo-kb
gh skill update --all
```

Pinned skills are skipped by normal update. Reinstall with a new `--pin` value when you want to move a pinned project forward.

Search for related skills:

```bash
gh skill search code-review
gh skill search repository-knowledge
```

## Publish

Publishing is not required for basic installation. Because this repository is public and follows the `skills/*/SKILL.md` convention, users can install directly from the repository:

```bash
gh skill install makikub/repo-knowledge-compiler repo-kb --agent claude-code --scope project
```

Use `gh skill publish` when you want GitHub CLI to validate the skill, add release-oriented metadata, choose a version tag, and create a GitHub release. This is useful when you want stable versioned installs such as `--pin v0.1.0`.

Validate without publishing:

```bash
gh skill publish --dry-run
```

Publish interactively:

```bash
gh skill publish
```

Publish non-interactively with a tag:

```bash
gh skill publish --tag v0.1.0
```

If validation reports fixable metadata issues, run:

```bash
gh skill publish --fix
```

Review and commit any changes from `--fix`, then run `gh skill publish --dry-run` again.

## Project Setup After Install

After installing the skill into a target repository, ask your agent:

```text
$repo-kb を使って、このリポジトリを初期化して
```

Users should not need to remember Python paths. In agent chat, describe intent directly:

```text
/repo-kb ingest DBトランザクション境界の教訓: 外部API呼び出しを中に入れない
/repo-kb ask DBトランザクション境界の注意点は？
/repo-kb promote 今月の安定した知識だけ CLAUDE.md / REVIEW.md / rules に反映して
```

The agent maps those requests to the skill workflow and runs deterministic helpers when useful. You can also run the helper directly from the installed skill directory. Depending on the agent and scope, `gh skill` places the skill under an agent-specific directory such as `.claude/skills/repo-kb/` or a shared project directory such as `.agents/skills/repo-kb/`.

Claude Code project install example:

```bash
.claude/skills/repo-kb/scripts/repo-kb init
.claude/skills/repo-kb/scripts/repo-kb lint
.claude/skills/repo-kb/scripts/repo-kb compile --check
```

Shared project install example:

```bash
.agents/skills/repo-kb/scripts/repo-kb init
.agents/skills/repo-kb/scripts/repo-kb lint
.agents/skills/repo-kb/scripts/repo-kb compile --check
```

This creates and manages:

```text
.repo-kb/
```

`CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, and other agent instruction files are not created, overwritten, or auto-populated. Ask the agent to update them intentionally during a separate maintenance task by consulting `.repo-kb/index.md`, relevant `.repo-kb/raw/` notes, `.repo-kb/generated/claude-context.md`, `.repo-kb/generated/review.md`, and `.repo-kb/generated/rule-references/`.

Commit both the installed project skill and the repository knowledge files when you want teammates and CI to use the same behavior.

## Optional Vendoring

If you installed `repo-kb` at user scope but want a checked-in project copy, use the bundled `vendor` command:

```bash
<installed-skill-dir>/scripts/repo-kb vendor --path .agents/skills/repo-kb --force
.agents/skills/repo-kb/scripts/repo-kb init
```

The usual update flow is:

```bash
gh skill update repo-kb
cd /path/to/target-repo
<installed-skill-dir>/scripts/repo-kb vendor --path .agents/skills/repo-kb --force
.agents/skills/repo-kb/scripts/repo-kb compile --check
```

If you installed directly at project scope with `gh skill install ... --scope project`, this vendoring step is usually unnecessary.

## Local Smoke Test

From this repository root:

```bash
skills/repo-kb/scripts/repo-kb init
skills/repo-kb/scripts/repo-kb vendor --path /private/tmp/repo-kb-vendor-smoke --force
skills/repo-kb/scripts/repo-kb ingest --kind human-note --title "Smoke note" --note "This is a smoke-test note."
skills/repo-kb/scripts/repo-kb lint
skills/repo-kb/scripts/repo-kb compile
skills/repo-kb/scripts/repo-kb compile --check
```

The smoke-test ingest writes to `.repo-kb/raw/human-notes/`; remove that generated note before publishing if you do not want it in the repository history.

## Target Repository Usage

Inside a target repository, first vendor the skill:

```bash
<installed-skill-dir>/scripts/repo-kb vendor --path .agents/skills/repo-kb
```

Then use the repo-local copy:

```bash
.agents/skills/repo-kb/scripts/repo-kb init
.agents/skills/repo-kb/scripts/repo-kb ingest --kind log --title "Debugging session" --note "Sanitized raw log."
.agents/skills/repo-kb/scripts/repo-kb ingest-directory --path docs/adr --glob "*.md" --kind adr
.agents/skills/repo-kb/scripts/repo-kb ingest-pr-comments --since 2026-05-01 --until 2026-05-07 --repo OWNER/REPO
.agents/skills/repo-kb/scripts/repo-kb lint
.agents/skills/repo-kb/scripts/repo-kb compile
.agents/skills/repo-kb/scripts/repo-kb compile --check
.agents/skills/repo-kb/scripts/repo-kb ask "What should I know before changing src/api?"
.agents/skills/repo-kb/scripts/repo-kb promote --target CLAUDE.md --target REVIEW.md
```

Use `$repo-kb` for semantic work such as deciding whether an ingested note has durable signal, merging it into existing pages, and promoting draft review aspects to active guidance.

For operational help:

```bash
.agents/skills/repo-kb/scripts/repo-kb operations
```

For weekly growth, ingest recent notes or selected directory snapshots, ingest PR comments for the target period, synthesize durable lessons into `.repo-kb/pages/` or `.repo-kb/review-aspects/`, then run lint and compile. `ingest-pr-comments` requires the `gh` CLI and stores PR review/conversation comments as raw review-comment evidence.

For weekly or monthly promotion into project guidance:

```text
$repo-kb を使って、.repo-kb の最近の raw/page/review-aspect を確認し、必要なものだけ CLAUDE.md / rules / docs に反映して
```

## Design Position

The plugin is intentionally repo-agnostic. It provides workflows, templates, and structural checks. Repository-specific raw logs, wiki pages, and review aspects live in each target repo's `.repo-kb/` and are reviewed like code.

Generated files should not become the source of truth or be copied into agent rules automatically. Update `.repo-kb/`, compile, then promote concise guidance only when needed.
