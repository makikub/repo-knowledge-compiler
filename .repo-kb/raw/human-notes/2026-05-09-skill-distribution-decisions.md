---
type: raw-source
kind: human-note
id: 2026-05-09-skill-distribution-decisions
date: 2026-05-09
source_ref: user-provided
---

# Skill distribution and dogfooding decisions

## Original or Sanitized Note

Important decisions from the setup conversation: repo-knowledge-compiler is published as a public GitHub repository at makikub/repo-knowledge-compiler and contains the repo-kb skill under skills/repo-kb. Users should preview before installing with gh skill preview makikub/repo-knowledge-compiler repo-kb. Direct install is possible from the public repository without gh skill publish. gh skill publish is optional and mainly used for validation, GitHub release/tag creation, and stable pinned installs such as --pin v0.1.0. gh skill publish --dry-run should pass before release; the skill frontmatter includes license: MIT for clean validation. Supported install examples include Claude Code project/user scope and Codex project scope. Project-scope installs may place the skill under agent-specific or shared directories; this repo documents .claude/skills/repo-kb and .agents/skills/repo-kb examples. Target repositories may keep a vendored copy of the skill so CI and collaborators use a stable repo-relative path. The vendor command copies the installed skill into .agents/skills/repo-kb, and the update flow is gh skill update repo-kb followed by vendor --force in target repositories. This repository itself should dogfood .repo-kb directly using skills/repo-kb/scripts/repo_kb.py and does not need vendoring. In this repository, .repo-kb records this repository's own operational knowledge, while skills/repo-kb/assets/templates/.repo-kb contains templates distributed to target repositories. If a dogfooded learning should affect all target repos, update SKILL.md, references, scripts, or assets/templates in addition to .repo-kb.

## Extracted Claims

- TODO: Extract durable claims, decisions, review triggers, and open questions.

## Integration Notes

- TODO: Link this source from related `.repo-kb/pages/` or `.repo-kb/review-aspects/`.
