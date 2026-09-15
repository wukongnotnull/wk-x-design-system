#!/usr/bin/env python3
"""Verify the distilled showcase snapshot still matches the skill contract."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = SKILL_ROOT / "showcase"
TOKENS = SHOWCASE / "tokens.css"
SKILL_MD = SKILL_ROOT / "SKILL.md"
EXAMPLES_MD = SKILL_ROOT / "examples.md"
SITE_CSS = SHOWCASE / "site.css"
INDEX_HTML = SHOWCASE / "index.html"

REQUIRED_FILES = (
    SHOWCASE / "tokens.css",
    SHOWCASE / "site.css",
    SHOWCASE / "index.html",
    SHOWCASE / "icons" / "manifest.json",
    SKILL_ROOT / "examples.md",
)

PINNED = {
    "--dark-background": "0 0 0",
    "--dim-background": "22 33 44",
    "--accent-blue": "29 155 240",
    "--accent-red": "244 33 46",
    "--main-accent": "var(--accent-blue)",
    "--twitter-icon": "#D6D9DB",
    "--radius-full": "9999px",
}

FORBIDDEN_IN_SKILL = (
    "Documents/others/x-design-system",
    "references/components.md",
    "references/tokens.css",
    "/Users/",
)

CODE = re.compile(r"`([^`]+)`")


def examples_rows(md: str) -> list[tuple[str, str, str]]:
    """Yield (task, markup hook cell, grep cell) for each data row of the table."""
    rows: list[tuple[str, str, str]] = []
    for line in md.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 4 or cols[0] == "Task":
            continue
        rows.append((cols[0], cols[2], cols[3]))
    return rows


def hook_present(hook: str, html: str) -> bool:
    head = hook.split()[0]
    if head.startswith("["):
        attr = head.strip("[]")
        if "=" in attr:
            name, value = attr.split("=", 1)
            return f'{name}={value}' in html
        return re.search(rf"\s{re.escape(attr)}[\s=>]", html) is not None
    if head.startswith(("#", ".")):
        key = head[1:]
        return f'id="{key}"' in html or key in html
    return head in html


def check_examples(md: str, css: str, html: str) -> list[str]:
    """Every examples.md row must resolve: hooks in index.html, selectors in site.css."""
    errors: list[str] = []
    for task, hook_cell, grep_cell in examples_rows(md):
        for hook in CODE.findall(hook_cell):
            if hook.startswith("showcase/"):
                continue
            if not hook_present(hook, html):
                errors.append(f"examples.md [{task}]: hook {hook} not in index.html")
        for sel in CODE.findall(grep_cell):
            head = sel if sel.startswith("@media") else sel.split()[0]
            if head not in css:
                errors.append(f"examples.md [{task}]: selector {sel} not in site.css")
    patterns = sorted(set(re.findall(r'data-pattern="([^"]+)"', html)))
    for pattern in patterns:
        if f'data-pattern="{pattern}"' not in md:
            errors.append(f'index.html data-pattern="{pattern}" has no examples.md row')
    return errors


def run_unittests() -> list[str]:
    modules = sorted(
        f"tests.{path.stem}" for path in (SHOWCASE / "tests").glob("test_*.py")
    )
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", *modules],
        cwd=SHOWCASE,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return ["showcase unittest failed:\n" + proc.stderr.strip()]
    summary = proc.stderr.strip().splitlines()
    return [] if not summary else [f"__ok__ {summary[-3]}"]


def decl(css: str, name: str) -> str:
    match = re.search(rf"{re.escape(name)}:\s*([^;]+);", css)
    if not match:
        raise SystemExit(f"missing {name} in showcase/tokens.css")
    return re.sub(r"\s+", " ", match.group(1).strip())


def main() -> int:
    missing = [str(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        print("missing files:")
        print("\n".join(missing))
        return 1

    css = TOKENS.read_text(encoding="utf-8")
    skill = SKILL_MD.read_text(encoding="utf-8")
    errors: list[str] = []

    for name, value in PINNED.items():
        got = decl(css, name)
        if got != value:
            errors.append(f"{name}: expected {value!r}, got {got!r}")

    if 'data-theme="lights-out"' not in (SHOWCASE / "index.html").read_text(
        encoding="utf-8"
    ):
        errors.append('showcase/index.html missing data-theme="lights-out"')

    if "62a9588" not in skill or "ccrsxx/twitter-clone" not in skill:
        errors.append("SKILL.md must pin ccrsxx/twitter-clone @ 62a9588")

    examples = EXAMPLES_MD.read_text(encoding="utf-8")
    for needle in FORBIDDEN_IN_SKILL:
        if needle in skill:
            errors.append(f"SKILL.md still mentions stale path {needle}")
        if needle in examples:
            errors.append(f"examples.md still mentions stale path {needle}")

    chirp = list(SHOWCASE.rglob("*chirp*")) + list(SHOWCASE.rglob("*.woff2"))
    if chirp:
        errors.append(f"Chirp/font files in showcase: {chirp}")

    if list(SHOWCASE.rglob("docs")):
        errors.append("process docs found under showcase/; keep the skill to runtime files")

    errors.extend(
        check_examples(
            examples,
            SITE_CSS.read_text(encoding="utf-8"),
            INDEX_HTML.read_text(encoding="utf-8"),
        )
    )

    unit = run_unittests()
    ok_line = next((line for line in unit if line.startswith("__ok__")), None)
    errors.extend(line for line in unit if not line.startswith("__ok__"))

    if errors:
        print("\n".join(errors))
        return 1

    print("showcase snapshot OK")
    if ok_line:
        print("unittest:", ok_line.removeprefix("__ok__ "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
