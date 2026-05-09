# Compiled Repo Context

This file is generated from `.repo-kb/`. Update knowledge pages, then run compile.

## Active Practices

- **Repo Knowledge Compiler concept**: Repo Knowledge Compiler adapts Karpathy's LLM Wiki pattern to software repositories. It is not generic documentation management; it is a durable repository knowledge system that turns PRs, review findings, incidents, ADRs, design decisio... Source: `.repo-kb/pages/architecture/repo-knowledge-compiler-concept.md`
- **Initial repository workflow**: Use `.repo-kb/` as the durable source for repository conventions, review aspects, design decisions, and operational lessons. Compile concise outputs from it instead of manually expanding agent instruction files. Source: `.repo-kb/pages/conventions/initial-repository-workflow.md`
- **Project guidance files**: `repo-kb init` must not create `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/`, or other agent instruction files, and `repo-kb compile` must not overwrite them. These files belong to each repository and should be updated intentio... Source: `.repo-kb/pages/conventions/project-guidance-files.md`
- **Skill distribution and dogfooding**: This repository is the upstream source for the `repo-kb` skill and also dogfoods `.repo-kb/` for its own operational knowledge. Public repository installs work directly through `gh skill`; `gh skill publish` is optional unless versioned... Source: `.repo-kb/pages/conventions/skill-distribution-and-dogfooding.md`
