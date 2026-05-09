#!/usr/bin/env python3
"""Minimal Repo Knowledge Compiler helper."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import subprocess
import textwrap
import datetime as dt
from pathlib import Path


ROOT = Path.cwd()
KB = ROOT / ".repo-kb"
SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"
RAW_DIRS = {
    "pr": "pr",
    "issue": "issues",
    "incident": "incidents",
    "adr": "adr",
    "review-comment": "review-comments",
    "log": "logs",
    "human-note": "human-notes",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def copy_template(relative: str, destination: Path) -> None:
    src = TEMPLATE_DIR / relative
    if not src.exists():
        raise SystemExit(f"missing template: {src}")
    if destination.exists():
        return
    if src.is_dir():
        shutil.copytree(src, destination, dirs_exist_ok=True)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, destination)


def command_init(_: argparse.Namespace) -> int:
    copy_template(".repo-kb", KB)
    print("initialized .repo-kb templates only")
    print("project guidance files and .claude/rules are not created automatically; use .repo-kb/generated/ as reference material")
    return 0


def command_vendor(args: argparse.Namespace) -> int:
    destination = ROOT / args.path
    if destination.resolve() == SKILL_DIR:
        raise SystemExit("destination is the current skill directory")
    if destination.exists():
        if not args.force:
            raise SystemExit(f"skill copy already exists: {destination}; pass --force to replace it")
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        SKILL_DIR,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", ".claude"),
    )
    print(f"vendored repo-kb skill to {display_path(destination)}")
    return 0


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "note"


def today() -> str:
    return dt.date.today().isoformat()


def read_note(args: argparse.Namespace) -> str:
    if args.file:
        return read(Path(args.file))
    if args.note:
        return args.note
    raise SystemExit("ingest requires --note or --file")


def append_log(message: str) -> None:
    path = KB / "log.md"
    existing = read(path) if path.exists() else "# Repo Knowledge Log\n"
    write(path, existing.rstrip() + "\n\n" + message.rstrip() + "\n")


def write_raw_source(
    *,
    kind: str,
    source_id: str,
    title: str,
    source_ref: str,
    note: str,
    force: bool = False,
) -> Path:
    if not KB.exists():
        command_init(argparse.Namespace())

    kind_dir = RAW_DIRS[kind]
    raw_path = KB / "raw" / kind_dir / f"{slugify(source_id)}.md"
    if raw_path.exists() and not force:
        raise SystemExit(f"raw source already exists: {raw_path.relative_to(ROOT)}; pass --force to overwrite")

    raw_text = f"""---
type: raw-source
kind: {kind}
id: {source_id}
date: {today()}
source_ref: {source_ref}
---

# {title}

## Original or Sanitized Note

{note.strip()}

## Extracted Claims

- TODO: Extract tentative claims, decisions, review triggers, and open questions.

## Integration Notes

- TODO: Link this source from related `.repo-kb/pages/` or `.repo-kb/review-aspects/`.
"""
    write(raw_path, raw_text)
    return raw_path


def command_ingest(args: argparse.Namespace) -> int:
    if not KB.exists():
        command_init(args)

    source_id = args.id or f"{today()}-{slugify(args.title)}"
    title = args.title
    note = read_note(args).strip()
    raw_path = write_raw_source(
        kind=args.kind,
        source_id=source_id,
        title=title,
        source_ref=args.source_ref or "user-provided",
        note=note,
        force=args.force,
    )

    created = [raw_path.relative_to(ROOT)]
    if args.as_review_aspect:
        aspect_id = slugify(args.aspect_id or args.title)
        category = slugify(args.category or "correctness")
        aspect_path = KB / "review-aspects" / category / f"{aspect_id}.md"
        if aspect_path.exists() and not args.force:
            raise SystemExit(f"review aspect already exists: {aspect_path.relative_to(ROOT)}; pass --force to overwrite")
        applies_to = args.applies_to or ["TODO: add path pattern"]
        questions = args.review_question or ["TODO: Add concrete review question."]
        aspect_text = "\n".join([
            "---",
            "type: review-aspect",
            f"id: {aspect_id}",
            f"title: {title}",
            f"severity: {args.severity}",
            "status: draft",
            "applies_to:",
            *[f'  - "{item}"' for item in applies_to],
            "sources:",
            f"  - kind: {args.kind}",
            f"    id: \"{source_id}\"",
            f"    path: \"{raw_path.relative_to(ROOT)}\"",
            f"last_verified: {today()}",
            "---",
            "",
            f"# {title}",
            "",
            "## Why this matters",
            "",
            textwrap.shorten(" ".join(note.split()), width=420, placeholder="..."),
            "",
            "## Review trigger",
            "",
            "- TODO: Describe when this aspect applies.",
            "",
            "## Review questions",
            "",
            *[f"- {question}" for question in questions],
            "",
            "## Good example",
            "",
            "TODO",
            "",
            "## Bad example",
            "",
            "TODO",
            "",
        ])
        write(aspect_path, aspect_text)
        created.append(aspect_path.relative_to(ROOT))

    append_log(
        "\n".join([
            f"## [{today()}] ingest | {title}",
            "",
            f"- Raw source: `{raw_path.relative_to(ROOT)}`",
            f"- Kind: `{args.kind}`",
            f"- Source id: `{source_id}`",
        ])
    )
    for path in created:
        print(f"created {path}")
    return 0


def run_gh_json(arguments: list[str]) -> object:
    try:
        result = subprocess.run(
            ["gh", *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise SystemExit("gh CLI is required for PR comment ingestion") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip()
        raise SystemExit(f"gh command failed: {detail}") from exc
    output = result.stdout.strip()
    if not output:
        return []
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"gh returned invalid JSON: {exc}") from exc


def current_repo_name() -> str:
    data = run_gh_json(["repo", "view", "--json", "nameWithOwner"])
    if not isinstance(data, dict) or not data.get("nameWithOwner"):
        raise SystemExit("could not determine repository; pass --repo OWNER/REPO")
    return str(data["nameWithOwner"])


def parse_instant(value: str, *, end_of_day: bool = False) -> dt.datetime:
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        parsed_date = dt.date.fromisoformat(value)
        parsed = dt.datetime.combine(parsed_date, dt.time.max if end_of_day else dt.time.min)
        return parsed.replace(tzinfo=dt.timezone.utc)
    normalized = value.replace("Z", "+00:00")
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def parse_github_time(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(dt.timezone.utc)


def in_period(value: str, since: dt.datetime, until: dt.datetime) -> bool:
    timestamp = parse_github_time(value)
    return since <= timestamp <= until


def github_timestamp(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def gh_paginated(path: str, repo: str, *, since: dt.datetime | None = None) -> list[dict[str, object]]:
    api_path = f"repos/{repo}/{path}"
    if since:
        api_path += f"?since={github_timestamp(since)}"
    data = run_gh_json(["api", "--paginate", "--slurp", api_path])
    if not isinstance(data, list):
        raise SystemExit(f"unexpected gh API response for {path}")
    if data and all(isinstance(item, list) for item in data):
        flattened: list[dict[str, object]] = []
        for page in data:
            flattened.extend(item for item in page if isinstance(item, dict))
        return flattened
    return [item for item in data if isinstance(item, dict)]


def issue_number_from_url(url: str) -> str:
    return url.rstrip("/").rsplit("/", 1)[-1]


def pull_request_numbers(repo: str, issue_numbers: set[str]) -> set[str]:
    pull_numbers: set[str] = set()
    for number in sorted(issue_numbers, key=int):
        issue = run_gh_json(["api", f"repos/{repo}/issues/{number}"])
        if isinstance(issue, dict) and issue.get("pull_request"):
            pull_numbers.add(number)
    return pull_numbers


def format_comment_item(item: dict[str, object]) -> str:
    user = item.get("user") if isinstance(item.get("user"), dict) else {}
    author = user.get("login", "unknown") if isinstance(user, dict) else "unknown"
    created = item.get("created_at", "unknown")
    url = item.get("html_url", "")
    body = str(item.get("body") or "").strip()
    parts = [f"- Author: `{author}`", f"- Created: `{created}`"]
    if url:
        parts.append(f"- URL: {url}")
    if item.get("path"):
        location = str(item.get("path"))
        if item.get("line"):
            location += f":{item.get('line')}"
        parts.append(f"- Location: `{location}`")
    return "\n".join([*parts, "", body or "(empty comment)"])


def collect_pr_comments(repo: str, since: dt.datetime, until: dt.datetime) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    review_comments = [
        item for item in gh_paginated("pulls/comments", repo, since=since)
        if isinstance(item.get("created_at"), str) and in_period(str(item["created_at"]), since, until)
    ]
    issue_comments = [
        item for item in gh_paginated("issues/comments", repo, since=since)
        if isinstance(item.get("created_at"), str) and in_period(str(item["created_at"]), since, until)
    ]
    candidate_numbers = {
        issue_number_from_url(str(item.get("issue_url")))
        for item in issue_comments
        if item.get("issue_url")
    }
    pr_numbers = pull_request_numbers(repo, candidate_numbers)
    pr_issue_comments = [
        item for item in issue_comments
        if issue_number_from_url(str(item.get("issue_url"))) in pr_numbers
    ]
    return review_comments, pr_issue_comments


def render_pr_comments_note(
    repo: str,
    since_label: str,
    until_label: str,
    review_comments: list[dict[str, object]],
    issue_comments: list[dict[str, object]],
) -> str:
    lines = [
        f"Repository: `{repo}`",
        f"Period: `{since_label}` to `{until_label}`",
        "",
        "This note was collected from GitHub PR review comments and PR conversation comments.",
        "",
        "## PR Review Comments",
        "",
    ]
    if not review_comments:
        lines.append("- No PR review comments found in this period.")
    for item in review_comments:
        lines.extend(["### Review comment", "", format_comment_item(item), ""])
    lines.extend(["", "## PR Conversation Comments", ""])
    if not issue_comments:
        lines.append("- No PR conversation comments found in this period.")
    for item in issue_comments:
        number = issue_number_from_url(str(item.get("issue_url", "")))
        lines.extend([f"### PR #{number} conversation comment", "", format_comment_item(item), ""])
    return "\n".join(lines).rstrip()


def command_ingest_pr_comments(args: argparse.Namespace) -> int:
    if not KB.exists():
        command_init(args)

    repo = args.repo or current_repo_name()
    since = parse_instant(args.since)
    until = parse_instant(args.until, end_of_day=True)
    if since > until:
        raise SystemExit("--since must be earlier than or equal to --until")

    review_comments, issue_comments = collect_pr_comments(repo, since, until)
    note = render_pr_comments_note(repo, args.since, args.until, review_comments, issue_comments)
    title = args.title or f"PR comments {repo} {args.since} to {args.until}"
    source_id = args.id or f"pr-comments-{repo.replace('/', '-')}-{args.since}-to-{args.until}"

    if args.dry_run:
        print(note)
        return 0

    raw_path = write_raw_source(
        kind="review-comment",
        source_id=source_id,
        title=title,
        source_ref=f"github:{repo}:pr-comments:{args.since}..{args.until}",
        note=note,
        force=args.force,
    )
    append_log(
        "\n".join([
            f"## [{today()}] ingest-pr-comments | {title}",
            "",
            f"- Raw source: `{raw_path.relative_to(ROOT)}`",
            f"- Repository: `{repo}`",
            f"- Period: `{args.since}` to `{args.until}`",
            f"- PR review comments: `{len(review_comments)}`",
            f"- PR conversation comments: `{len(issue_comments)}`",
        ])
    )
    print(f"created {raw_path.relative_to(ROOT)}")
    print(f"collected {len(review_comments)} PR review comments and {len(issue_comments)} PR conversation comments")
    return 0


def directory_files(path: Path, pattern: str) -> list[Path]:
    if path.is_file():
        return [path]
    if not path.exists():
        raise SystemExit(f"ingest directory path does not exist: {path}")
    if not path.is_dir():
        raise SystemExit(f"ingest directory path is not a file or directory: {path}")
    return sorted(file_path for file_path in path.rglob(pattern) if file_path.is_file())


def render_directory_note(source_path: Path, files: list[Path], max_bytes: int) -> str:
    lines = [
        f"Source path: `{display_path(source_path)}`",
        f"Files captured: `{len(files)}`",
        "",
        "This note was collected from repository files for periodic repo-kb ingestion.",
        "",
    ]
    if not files:
        lines.append("- No files matched the requested path and pattern.")
        return "\n".join(lines)
    for file_path in files:
        rel = display_path(file_path)
        data = file_path.read_bytes()
        truncated = len(data) > max_bytes
        text = data[:max_bytes].decode("utf-8", errors="replace")
        lines.extend([
            f"## `{rel}`",
            "",
            "```text",
            text.rstrip(),
            "```",
            "",
        ])
        if truncated:
            lines.extend([f"_Truncated after {max_bytes} bytes._", ""])
    return "\n".join(lines).rstrip()


def command_ingest_directory(args: argparse.Namespace) -> int:
    if not KB.exists():
        command_init(args)

    source_path = Path(args.path)
    files = directory_files(source_path, args.glob)
    if len(files) > args.max_files and not args.force:
        raise SystemExit(f"{len(files)} files matched; pass --max-files or --force to ingest anyway")
    selected = files if args.force else files[: args.max_files]
    title = args.title or f"Directory ingest {display_path(source_path)}"
    source_id = args.id or f"{today()}-{slugify(title)}"
    note = render_directory_note(source_path, selected, args.max_bytes)

    raw_path = write_raw_source(
        kind=args.kind,
        source_id=source_id,
        title=title,
        source_ref=f"repo-path:{display_path(source_path)}",
        note=note,
        force=args.force,
    )
    append_log(
        "\n".join([
            f"## [{today()}] ingest-directory | {title}",
            "",
            f"- Raw source: `{raw_path.relative_to(ROOT)}`",
            f"- Source path: `{display_path(source_path)}`",
            f"- Glob: `{args.glob}`",
            f"- Files captured: `{len(selected)}`",
        ])
    )
    print(f"created {raw_path.relative_to(ROOT)}")
    print(f"captured {len(selected)} files from {display_path(source_path)}")
    return 0


def command_operations(_: argparse.Namespace) -> int:
    print(
        textwrap.dedent(
            """
            Repo KB operating model

            1. Capture raw evidence first.
               - Individual note or file:
                 python3 .agents/skills/repo-kb/scripts/repo_kb.py ingest --kind human-note --title "Title" --note "Sanitized note"
                 python3 .agents/skills/repo-kb/scripts/repo_kb.py ingest --kind log --title "Session log" --file /path/to/sanitized.md
               - Repository directory snapshot:
                 python3 .agents/skills/repo-kb/scripts/repo_kb.py ingest-directory --path docs/adr --glob "*.md" --kind adr
               - PR comments for a period:
                 python3 .agents/skills/repo-kb/scripts/repo_kb.py ingest-pr-comments --since YYYY-MM-DD --until YYYY-MM-DD --repo OWNER/REPO

            2. Synthesize durable lessons.
               Ask an agent to read recent .repo-kb/raw notes, update existing pages before creating new pages, and draft review aspects only when the lesson is repeatable.

            3. Compile and lint weekly.
               python3 .agents/skills/repo-kb/scripts/repo_kb.py lint
               python3 .agents/skills/repo-kb/scripts/repo_kb.py compile
               python3 .agents/skills/repo-kb/scripts/repo_kb.py compile --check

            4. Promote intentionally.
               Weekly or monthly, ask an agent to consult .repo-kb/index.md, raw notes, pages, review aspects, and generated references, then open a PR that updates only the concise guidance needed in CLAUDE.md, AGENTS.md, REVIEW.md, .claude/rules, or docs.

            Suggested weekly agent prompt:
              $repo-kb を使って、直近1週間の .repo-kb/raw とPRコメント取り込み結果を確認し、再発防止に効くものだけ pages/review-aspects に反映して。最後に lint と compile --check を実行して。

            Suggested monthly promotion prompt:
              $repo-kb を使って、.repo-kb のactiveな知識とgeneratedを確認し、CLAUDE.md / REVIEW.md / rules / docs に反映すべき高シグナルなものだけPR化して。
            """
        ).strip()
    )
    return 0


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].splitlines()
    data: dict[str, object] = {}
    current_key = None
    for line in raw:
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, [])
            value = line[4:].strip().strip('"')
            if isinstance(data[current_key], list):
                data[current_key].append(value)
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        current_key = key
        if value == "":
            data[key] = []
        else:
            data[key] = value.strip('"')
    return data, text[end + 5 :]


def markdown_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(path.rglob("*.md"))


def lint_errors() -> list[str]:
    errors: list[str] = []
    required = ["SCHEMA.md", "config.yaml", "index.md", "log.md"]
    for item in required:
        if not (KB / item).exists():
            errors.append(f"missing .repo-kb/{item}")

    for path in markdown_files(KB / "pages") + markdown_files(KB / "review-aspects"):
        meta, _ = parse_frontmatter(read(path))
        if not meta:
            errors.append(f"{path}: missing frontmatter")
            continue
        for key in ("type", "id", "title", "status"):
            if key not in meta:
                errors.append(f"{path}: missing frontmatter key {key}")
        if meta.get("type") == "review-aspect":
            if not meta.get("applies_to"):
                errors.append(f"{path}: review aspect missing applies_to")
            if not meta.get("sources"):
                errors.append(f"{path}: review aspect missing sources")

    for path in markdown_files(KB):
        text = read(path)
        for link in re.findall(r"\]\(([^)]+\.md)\)", text):
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            target = (path.parent / link).resolve()
            if not target.exists():
                errors.append(f"{path}: broken link {link}")
    return errors


def command_lint(_: argparse.Namespace) -> int:
    errors = lint_errors()
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("repo-kb lint passed")
    return 0


def active_markdown(path: Path, page_type: str | None = None) -> list[tuple[Path, dict[str, object], str]]:
    pages = []
    for file_path in markdown_files(path):
        meta, body = parse_frontmatter(read(file_path))
        if meta.get("status") != "active":
            continue
        if page_type and meta.get("type") != page_type:
            continue
        pages.append((file_path, meta, body.strip()))
    return pages


def first_section(body: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, body, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return match.group("body").strip()


def compile_claude_context() -> str:
    lines = [
        "# Compiled Repo Context",
        "",
        "This file is generated from `.repo-kb/`. Update knowledge pages, then run compile.",
        "",
        "## Active Practices",
        "",
    ]
    pages = active_markdown(KB / "pages")
    if not pages:
        lines.append("- No active knowledge pages yet.")
    for path, meta, body in pages:
        summary = first_section(body, "Summary") or first_section(body, "Current Practice")
        summary = " ".join(summary.split())
        if len(summary) > 240:
            summary = summary[:237].rstrip() + "..."
        rel = path.relative_to(ROOT)
        lines.append(f"- **{meta.get('title', path.stem)}**: {summary or 'See source page.'} Source: `{rel}`")
    lines.append("")
    return "\n".join(lines)


def compile_review() -> str:
    lines = [
        "# Review Guidance",
        "",
        "This file is generated from `.repo-kb/review-aspects/`. Update review aspects, then run compile.",
        "",
        "## High-Priority Checks",
        "",
    ]
    aspects = active_markdown(KB / "review-aspects", "review-aspect")
    if not aspects:
        lines.append("- No active review aspects yet.")
    for path, meta, body in aspects:
        applies = meta.get("applies_to", [])
        if isinstance(applies, str):
            applies = [applies]
        questions = first_section(body, "Review questions")
        bullets = [line.strip() for line in questions.splitlines() if line.strip().startswith("- ")]
        rel = path.relative_to(ROOT)
        lines.extend([
            f"### {meta.get('title', path.stem)}",
            f"Severity: `{meta.get('severity', 'medium')}`",
            f"Applies to: {', '.join(f'`{item}`' for item in applies) or '`unspecified`'}",
            "",
        ])
        if bullets:
            lines.extend(bullets)
        else:
            lines.append("- Review the source aspect before commenting.")
        lines.extend([f"Source: `{rel}`", ""])
    return "\n".join(lines)


def compile_rule_references() -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    for path, meta, body in active_markdown(KB / "review-aspects", "review-aspect"):
        applies = meta.get("applies_to", [])
        if isinstance(applies, str):
            applies = [applies]
        if not applies:
            continue
        slug = str(meta.get("id") or path.stem)
        questions = first_section(body, "Review questions")
        lines = ["---", "paths:"]
        lines.extend(f'  - "{pattern}"' for pattern in applies)
        lines.extend([
            "---",
            "",
            f"# {meta.get('title', slug)}",
            "",
            "Reference generated from `.repo-kb/review-aspects/`. If this should become an agent rule, ask an LLM to intentionally update the project rule file.",
            "",
        ])
        lines.append(questions or "Review the source aspect before making changes in these paths.")
        outputs[KB / "generated" / "rule-references" / f"{slug}.md"] = "\n".join(lines).rstrip() + "\n"
    return outputs


def desired_outputs() -> dict[Path, str]:
    outputs = {
        KB / "generated" / "claude-context.md": compile_claude_context(),
        KB / "generated" / "review.md": compile_review(),
    }
    outputs.update(compile_rule_references())
    return outputs


def stale_generated_outputs(desired: dict[Path, str]) -> list[Path]:
    managed_dirs = [
        KB / "generated" / "rules",
        KB / "generated" / "rule-references",
    ]
    desired_paths = set(desired)
    stale: list[Path] = []
    for directory in managed_dirs:
        for path in markdown_files(directory):
            if path not in desired_paths:
                stale.append(path)
    return sorted(stale)


def command_compile(args: argparse.Namespace) -> int:
    outputs = desired_outputs()
    stale_outputs = stale_generated_outputs(outputs)
    drift = False
    for path, text in outputs.items():
        if args.check:
            existing = read(path) if path.exists() else ""
            if existing != text:
                drift = True
                print(f"DRIFT {path.relative_to(ROOT)}")
                diff = difflib.unified_diff(
                    existing.splitlines(),
                    text.splitlines(),
                    fromfile=str(path.relative_to(ROOT)),
                    tofile="compiled",
                    lineterm="",
                )
                for line in list(diff)[:80]:
                    print(line)
            continue
        write(path, text)
    for path in stale_outputs:
        if args.check:
            drift = True
            print(f"STALE {path.relative_to(ROOT)}")
            continue
        path.unlink()
    if args.check and drift:
        return 1
    print("repo-kb compile passed" if args.check else "compiled repo-kb outputs")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="repo_kb.py")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.set_defaults(func=command_init)
    vendor = sub.add_parser("vendor")
    vendor.add_argument("--path", default=".agents/skills/repo-kb")
    vendor.add_argument("--force", action="store_true")
    vendor.set_defaults(func=command_vendor)
    ingest = sub.add_parser("ingest")
    ingest.add_argument("--kind", choices=sorted(RAW_DIRS), default="human-note")
    ingest.add_argument("--id")
    ingest.add_argument("--title", required=True)
    ingest.add_argument("--source-ref")
    ingest.add_argument("--note")
    ingest.add_argument("--file")
    ingest.add_argument("--force", action="store_true")
    ingest.add_argument("--as-review-aspect", action="store_true")
    ingest.add_argument("--aspect-id")
    ingest.add_argument("--category", default="correctness")
    ingest.add_argument("--severity", choices=["high", "medium", "low"], default="medium")
    ingest.add_argument("--applies-to", action="append")
    ingest.add_argument("--review-question", action="append")
    ingest.set_defaults(func=command_ingest)
    ingest_directory = sub.add_parser(
        "ingest-directory",
        help="capture matching files under a repository path as a raw source",
    )
    ingest_directory.add_argument("--path", required=True, help="file or directory to capture")
    ingest_directory.add_argument("--glob", default="*.md", help="rglob pattern used when --path is a directory")
    ingest_directory.add_argument("--kind", choices=sorted(RAW_DIRS), default="log")
    ingest_directory.add_argument("--id")
    ingest_directory.add_argument("--title")
    ingest_directory.add_argument("--max-files", type=int, default=50)
    ingest_directory.add_argument("--max-bytes", type=int, default=20000)
    ingest_directory.add_argument("--force", action="store_true")
    ingest_directory.set_defaults(func=command_ingest_directory)
    ingest_pr_comments = sub.add_parser(
        "ingest-pr-comments",
        help="collect GitHub PR comments for a period and ingest them as a raw review-comment source",
    )
    ingest_pr_comments.add_argument("--repo", help="GitHub repository as OWNER/REPO; defaults to gh repo view")
    ingest_pr_comments.add_argument("--since", required=True, help="inclusive start date or timestamp, for example 2026-05-01")
    ingest_pr_comments.add_argument("--until", required=True, help="inclusive end date or timestamp, for example 2026-05-07")
    ingest_pr_comments.add_argument("--id")
    ingest_pr_comments.add_argument("--title")
    ingest_pr_comments.add_argument("--force", action="store_true")
    ingest_pr_comments.add_argument("--dry-run", action="store_true")
    ingest_pr_comments.set_defaults(func=command_ingest_pr_comments)
    lint = sub.add_parser("lint")
    lint.set_defaults(func=command_lint)
    compile_cmd = sub.add_parser("compile")
    compile_cmd.add_argument("--check", action="store_true")
    compile_cmd.set_defaults(func=command_compile)
    operations = sub.add_parser("operations", help="print recommended repo-kb operating workflows")
    operations.set_defaults(func=command_operations)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
