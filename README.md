# Repo Knowledge Compiler

Repo Knowledge Compiler adapts Karpathy's LLM Wiki pattern to software repositories.

Instead of putting every project rule into `CLAUDE.md` or `AGENTS.md`, each target repository keeps durable operational knowledge in `.repo-kb/`:

- PR and review lessons
- incidents and bug patterns
- architecture decisions
- conventions and invariants
- code-review aspects
- generated agent guidance

The skill then compiles that knowledge into concise outputs such as `CLAUDE.md`, `REVIEW.md`, and `.claude/rules/generated/`.

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

Or run the helper directly from the installed skill directory. Depending on the agent and scope, `gh skill` places the skill under an agent-specific directory such as `.claude/skills/repo-kb/` or a shared project directory such as `.agents/skills/repo-kb/`.

Claude Code project install example:

```bash
python3 .claude/skills/repo-kb/scripts/repo_kb.py init
python3 .claude/skills/repo-kb/scripts/repo_kb.py lint
python3 .claude/skills/repo-kb/scripts/repo_kb.py compile --check
```

Shared project install example:

```bash
python3 .agents/skills/repo-kb/scripts/repo_kb.py init
python3 .agents/skills/repo-kb/scripts/repo_kb.py lint
python3 .agents/skills/repo-kb/scripts/repo_kb.py compile --check
```

This creates and manages:

```text
.repo-kb/
CLAUDE.md
REVIEW.md
.claude/rules/generated/
```

Commit both the installed project skill and the generated repository knowledge files when you want teammates and CI to use the same behavior.

## Optional Vendoring

If you installed `repo-kb` at user scope but want a checked-in project copy, use the bundled `vendor` command:

```bash
python3 <installed-skill-dir>/scripts/repo_kb.py vendor --path .agents/skills/repo-kb --force
python3 .agents/skills/repo-kb/scripts/repo_kb.py init
```

The usual update flow is:

```bash
gh skill update repo-kb
cd /path/to/target-repo
python3 <installed-skill-dir>/scripts/repo_kb.py vendor --path .agents/skills/repo-kb --force
python3 .agents/skills/repo-kb/scripts/repo_kb.py compile --check
```

If you installed directly at project scope with `gh skill install ... --scope project`, this vendoring step is usually unnecessary.

## Local Smoke Test

From this repository root:

```bash
python3 skills/repo-kb/scripts/repo_kb.py init
python3 skills/repo-kb/scripts/repo_kb.py vendor --path /private/tmp/repo-kb-vendor-smoke --force
python3 skills/repo-kb/scripts/repo_kb.py ingest --kind human-note --title "Smoke note" --note "This is a smoke-test note."
python3 skills/repo-kb/scripts/repo_kb.py lint
python3 skills/repo-kb/scripts/repo_kb.py compile
python3 skills/repo-kb/scripts/repo_kb.py compile --check
```

The smoke-test ingest writes to `.repo-kb/raw/human-notes/`; remove that generated note before publishing if you do not want it in the repository history.

## Target Repository Usage

Inside a target repository, first vendor the skill:

```bash
python3 <installed-skill-dir>/scripts/repo_kb.py vendor --path .agents/skills/repo-kb
```

Then use the repo-local copy:

```bash
python3 .agents/skills/repo-kb/scripts/repo_kb.py init
python3 .agents/skills/repo-kb/scripts/repo_kb.py ingest --kind human-note --title "Review lesson" --note "Sanitized note."
python3 .agents/skills/repo-kb/scripts/repo_kb.py lint
python3 .agents/skills/repo-kb/scripts/repo_kb.py compile
python3 .agents/skills/repo-kb/scripts/repo_kb.py compile --check
```

Use `$repo-kb` for semantic work such as deciding where an ingested note belongs, merging it into existing pages, and promoting draft review aspects to active guidance.

## Design Position

The plugin is intentionally repo-agnostic. It provides workflows, templates, and structural checks. Repository-specific knowledge lives in each target repo's `.repo-kb/` and is reviewed like code.

Generated files should not become the source of truth. Update `.repo-kb/`, then compile.
