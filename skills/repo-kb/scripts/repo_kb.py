#!/usr/bin/env python3
"""Minimal Repo Knowledge Compiler helper."""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
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
    print("initialized .repo-kb templates")
    print("project guidance files are not created automatically; use .repo-kb/generated/ as reference material")
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
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
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


def command_ingest(args: argparse.Namespace) -> int:
    if not KB.exists():
        command_init(args)

    kind_dir = RAW_DIRS[args.kind]
    source_id = args.id or f"{today()}-{slugify(args.title)}"
    title = args.title
    note = read_note(args).strip()
    raw_path = KB / "raw" / kind_dir / f"{slugify(source_id)}.md"
    if raw_path.exists() and not args.force:
        raise SystemExit(f"raw source already exists: {raw_path.relative_to(ROOT)}; pass --force to overwrite")

    raw_text = f"""---
type: raw-source
kind: {args.kind}
id: {source_id}
date: {today()}
source_ref: {args.source_ref or "user-provided"}
---

# {title}

## Original or Sanitized Note

{note}

## Extracted Claims

- TODO: Extract durable claims, decisions, review triggers, and open questions.

## Integration Notes

- TODO: Link this source from related `.repo-kb/pages/` or `.repo-kb/review-aspects/`.
"""
    write(raw_path, raw_text)

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
        outputs[KB / "generated" / "rules" / f"{slug}.md"] = "\n".join(lines).rstrip() + "\n"
    return outputs


def desired_outputs() -> dict[Path, str]:
    outputs = {
        KB / "generated" / "claude-context.md": compile_claude_context(),
        KB / "generated" / "review.md": compile_review(),
    }
    outputs.update(compile_rule_references())
    return outputs


def command_compile(args: argparse.Namespace) -> int:
    outputs = desired_outputs()
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
    lint = sub.add_parser("lint")
    lint.set_defaults(func=command_lint)
    compile_cmd = sub.add_parser("compile")
    compile_cmd.add_argument("--check", action="store_true")
    compile_cmd.set_defaults(func=command_compile)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
