---
type: knowledge-page
id: skill-distribution-and-dogfooding
title: Skill distribution and dogfooding
status: active
sources:
  - kind: human-note
    id: 2026-05-09-skill-distribution-decisions
    path: .repo-kb/raw/human-notes/2026-05-09-skill-distribution-decisions.md
last_verified: 2026-05-09
---

# Skill distribution and dogfooding

## Summary

This repository is the upstream source for the `repo-kb` skill and also dogfoods `.repo-kb/` for its own operational knowledge. Public repository installs work directly through `gh skill`; `gh skill publish` is optional unless versioned release metadata is desired.

## Current Practice

- The upstream skill lives at `skills/repo-kb/`.
- The public GitHub repository is `makikub/repo-knowledge-compiler`.
- Users should inspect before installing with `gh skill preview makikub/repo-knowledge-compiler repo-kb`.
- Direct install from the public repository is supported without running `gh skill publish`.
- `gh skill publish --dry-run` should pass before a release.
- `gh skill publish --tag <version>` is used when creating a GitHub release/tag for pinned installs.
- Target repositories may keep a vendored copy at `.agents/skills/repo-kb/`.
- The update flow for vendored target repositories is `gh skill update repo-kb`, then `vendor --force` in each target repository.
- This repository does not need vendoring; it uses `skills/repo-kb/scripts/repo_kb.py` directly.

## Rationale

Keeping the GitHub repository as the update source lets `gh skill update` track upstream changes. Allowing target repositories to vendor the skill gives CI and collaborators a stable repo-relative execution path.

`gh skill publish` validates and creates release-oriented metadata, but direct public repository installs are enough for normal use. Releases become important when users want stable pins such as `--pin v0.1.0`.

## Repository Boundary

- `.repo-kb/` records operational knowledge for this repository itself.
- `skills/repo-kb/assets/templates/.repo-kb/` contains initial knowledge-base templates distributed to target repositories.
- Dogfooded lessons that should affect all target repositories must be reflected in `SKILL.md`, `references/`, `scripts/`, or `assets/templates/`, not only in this repository's `.repo-kb/`.

## Related Pages

- [Initial repository workflow](initial-repository-workflow.md)

## Open Questions

- Which release version should be used for the first published tag?
