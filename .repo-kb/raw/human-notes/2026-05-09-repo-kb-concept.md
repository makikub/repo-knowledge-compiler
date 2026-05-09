---
type: raw-source
kind: human-note
id: 2026-05-09-repo-kb-concept
date: 2026-05-09
source_ref: user-provided
---

# Repo Knowledge Compiler concept

## Original or Sanitized Note

Core motivation and design intent from the initial discussion: Adapt Karpathy's LLM Wiki pattern to development repositories. The goal is not generic documentation management but a continuously maintained repository knowledge system that absorbs PRs, review comments, incidents, ADRs, design decisions, conventions, tests, path-specific constraints, and team tacit knowledge. The durable knowledge base should live in repository-owned Markdown under .repo-kb, while concise outputs are compiled into agent-facing files such as CLAUDE.md, AGENTS.md, REVIEW.md, .claude/rules/generated, and possibly repo-specific review skills. CLAUDE.md should stay a short bootstrap, not become a giant wiki; detailed and evolving knowledge belongs in .repo-kb pages and review-aspects. Review guidance should grow from historical evidence, especially repeated review findings and incidents, and should compile into REVIEW.md and path-scoped rules. The system should separate raw sources, synthesized knowledge pages, and generated outputs. Raw sources should be treated as evidence and should not be silently rewritten. LLMs should do semantic synthesis and contradiction handling, while deterministic scripts handle structure, lint, and compile checks. The plugin/skill should be repo-agnostic and contain operations and templates, not repository-specific rules. Target repositories own their .repo-kb/config.yaml, SCHEMA.md, pages, review-aspects, and generated outputs. Safety principles: require sources for strong claims, avoid storing secrets or personal/customer data, record unresolved contradictions instead of hiding them, deprecate old rules rather than deleting useful history, and review knowledge changes through normal PR review. MVP priorities: init, ingest, lint, compile, review-pr, and CI compile --check; advanced MCP/search can come later.

## Extracted Claims

- TODO: Extract durable claims, decisions, review triggers, and open questions.

## Integration Notes

- TODO: Link this source from related `.repo-kb/pages/` or `.repo-kb/review-aspects/`.
