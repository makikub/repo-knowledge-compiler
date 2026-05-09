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

## Install And Update

This repository is intended to be installed from GitHub with `gh skill` and updated the same way. Target repositories may also keep a vendored copy of the skill so CI and local automation can use a stable repo-relative path.

```bash
gh skill install OWNER/repo-knowledge-compiler
gh skill update repo-kb
```

Replace `OWNER` with the GitHub owner after publishing this repository.

Recommended target-repo update flow:

```bash
gh skill update repo-kb
cd /path/to/target-repo
python3 <installed-skill-dir>/scripts/repo_kb.py vendor --path .agents/skills/repo-kb --force
```

Commit the vendored `.agents/skills/repo-kb/` copy when you want repeatable CI behavior or when collaborators should share the same skill version. Commit `.repo-kb/` and generated outputs as normal repository knowledge.

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
