---
type: knowledge-page
id: repo-knowledge-compiler-concept
title: Repo Knowledge Compiler concept
status: active
sources:
  - kind: human-note
    id: 2026-05-09-repo-kb-concept
    path: .repo-kb/raw/human-notes/2026-05-09-repo-kb-concept.md
last_verified: 2026-05-09
---

# Repo Knowledge Compiler concept

## Summary

Repo Knowledge Compiler adapts Karpathy's LLM Wiki pattern to software repositories. It is not generic documentation management; it is a durable repository knowledge system that turns PRs, review findings, incidents, ADRs, design decisions, conventions, and tacit team knowledge into maintainable Markdown and concise agent-facing outputs.

## Current Practice

- Keep durable repository knowledge in `.repo-kb/`.
- Treat raw sources as evidence and avoid silently rewriting them.
- Let LLMs synthesize meaning, merge related lessons, and surface contradictions.
- Let deterministic scripts handle structure, linting, reproducible compilation, and drift checks.
- Compile concise outputs into `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.claude/rules/generated/`, and related agent guidance.
- Keep `CLAUDE.md` as a short bootstrap instead of a large wiki.
- Grow review guidance from repeated review findings, incidents, and explicit team decisions.
- Keep the reusable skill repo-agnostic; target repositories own their `.repo-kb/` content.

## Rationale

RAG-style workflows often rediscover knowledge from raw documents every time. This project instead keeps a persistent, curated Markdown knowledge base that agents can incrementally maintain and compile into the right operational surfaces.

Development repositories need this because important guidance rarely lives in one place. It is scattered across PR comments, incidents, ADRs, old reviews, conventions, and local memory. `.repo-kb/` gives that knowledge a reviewed, versioned home while keeping agent startup context small.

## Architecture

The intended three-layer model is:

- `raw/`: immutable or minimally edited source evidence such as PR notes, review comments, incident summaries, ADRs, and sanitized human notes.
- `pages/` and `review-aspects/`: synthesized Markdown knowledge maintained by agents and reviewed by humans.
- `generated/` and top-level guidance files: reproducible compiled outputs for agents and reviews.

The reusable skill should provide operations, templates, and helper scripts. It should not contain project-specific rules. Each target repository owns its `config.yaml`, `SCHEMA.md`, knowledge pages, review aspects, and generated outputs.

## Review Knowledge

Review guidance should be more than a static checklist. A review aspect should explain why it matters, when it triggers, what questions reviewers should ask, and what examples clarify the rule.

Strong review claims should have sources unless they are explicitly marked as team policy. Old rules should be deprecated rather than erased when historical context remains useful.

## Safety Principles

- Do not store secrets, customer data, or personal data in raw sources.
- Require sources for strong claims.
- Record unresolved contradictions instead of hiding them.
- Review `.repo-kb/` changes through normal pull request review.
- Do not let agents freely rewrite their own top-level instructions without a source-backed knowledge update.

## MVP Direction

The first useful implementation should cover:

- `init`
- `ingest`
- `lint`
- `compile`
- `review-pr`
- CI checks for `lint` and `compile --check`

More advanced search, MCP integrations, and external data ingestion can come later.

## Related Pages

- [Initial repository workflow](../conventions/initial-repository-workflow.md)
- [Skill distribution and dogfooding](../conventions/skill-distribution-and-dogfooding.md)

## Open Questions

- How much of `review-pr` should be deterministic path matching versus agent judgment?
- Which external sources should be supported first after local notes and review comments?
