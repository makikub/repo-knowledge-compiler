# Repo Knowledge Index

## Architecture

- [Repo Knowledge Compiler concept](pages/architecture/repo-knowledge-compiler-concept.md): Why this project exists and how it adapts the LLM Wiki pattern to repository operations.

## Raw Sources

- Store PR notes, review comments, incidents, debugging logs, design discussions, and human notes under `raw/` first.

## Conventions

- [Initial repository workflow](pages/conventions/initial-repository-workflow.md): Bootstrap conventions for using `.repo-kb`.
- [Page synthesis workflow](pages/conventions/page-synthesis-workflow.md): Pages are never auto-generated. After ingest, the LLM must decide whether durable signal warrants creating or updating a page.
- [Project guidance files](pages/conventions/project-guidance-files.md): Agent instruction files are LLM-maintained from `.repo-kb` references, not created or overwritten by init/compile.
- [Skill distribution and dogfooding](pages/conventions/skill-distribution-and-dogfooding.md): How this skill is installed, optionally published, vendored into target repositories, and dogfooded here.

## Review Aspects

- [Knowledge promotion drift](review-aspects/correctness/knowledge-promotion-drift.md): Ensure project guidance updates are intentionally promoted from `.repo-kb` sources.
