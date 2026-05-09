# Compiled Repo Context

This file is generated from `.repo-kb/`. Update knowledge pages, then run compile.

## Active Practices

- **Repo Knowledge Compiler concept**: Repo Knowledge Compiler adapts Karpathy's LLM Wiki pattern to software repositories. It is not generic documentation management; it is a durable repository memory system where raw PR notes, review findings, incidents, ADRs, design discus... Source: `.repo-kb/pages/architecture/repo-knowledge-compiler-concept.md`
- **Project guidance files**: `repo-kb init` must not create `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or other agent instruction files, and `repo-kb compile` must not overwrite or auto-populate them. These files belong to each repository and should be... Source: `.repo-kb/pages/conventions/project-guidance-files.md`
- **Skill distribution and dogfooding**: This repository is the upstream source for the `repo-kb` skill and also dogfoods `.repo-kb/` for its own operational knowledge. Public repository installs work directly through `gh skill`; `gh skill publish` is optional unless versioned... Source: `.repo-kb/pages/conventions/skill-distribution-and-dogfooding.md`
