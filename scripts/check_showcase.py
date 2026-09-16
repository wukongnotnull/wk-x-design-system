#!/usr/bin/env python3
"""Verify the distilled showcase snapshot still matches the skill contract."""

from __future__ import annotations

import json
import re
import shutil
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
ICONS_DIR = SHOWCASE / "icons"
MANIFEST = ICONS_DIR / "manifest.json"

REQUIRED_FILES = (
    SHOWCASE / "tokens.css",
    SHOWCASE / "site.css",
    SHOWCASE / "index.html",
    MANIFEST,
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
    "C:\\",
    "\\\\",
)

ALLOWED_ICON_SOURCES = {
    "heroicons@2.0.11",
    "custom-icon.tsx@62a9588",
    "x.com logged-in extract 2026-09-16",
}

NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
CODE = re.compile(r"`([^`]+)`")
RAN_TESTS = re.compile(r"Ran \d+ tests in [0-9.]+s")
FRONTMATTER = re.compile(
    r"^---\n(.*?)\n---\n(.*)\Z",
    re.DOTALL,
)


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
            return f"{name}={value}" in html
        return re.search(rf"\s{re.escape(attr)}[\s=>]", html) is not None
    if head.startswith("#"):
        return bool(re.search(rf"""id=["']{re.escape(head[1:])}["']""", html))
    if head.startswith("."):
        key = head[1:]
        return bool(
            re.search(rf"""class=["'][^"']*\b{re.escape(key)}\b""", html)
        )
    return head in html


def selector_in_css(sel: str, css: str) -> bool:
    """The full selector must appear as a rule (before `{`), not a first-token substring."""
    compact = re.sub(r"\s+", " ", sel.strip())
    escaped = re.escape(compact).replace(r"\ ", r"\s+")
    if sel.startswith("@media"):
        return re.search(escaped + r"\s*\{", css) is not None
    return re.search(escaped + r"(?![A-Za-z0-9_-])[^{;]*\{", css) is not None


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
            if not selector_in_css(sel, css):
                errors.append(f"examples.md [{task}]: selector {sel} not in site.css")
    patterns = sorted(set(re.findall(r'data-pattern="([^"]+)"', html)))
    for pattern in patterns:
        if f'data-pattern="{pattern}"' not in md:
            errors.append(f'index.html data-pattern="{pattern}" has no examples.md row')
    controls = sorted(set(re.findall(r'data-control="([^"]+)"', html)))
    for control in controls:
        if f'data-control="{control}"' not in md:
            errors.append(f'index.html data-control="{control}" has no examples.md row')
    return errors


def check_icon_manifest() -> list[str]:
    errors: list[str] = []
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    listed: set[str] = set()
    for item in data.get("icons", []):
        ident = item.get("id", "<missing id>")
        source = item.get("source")
        if source not in ALLOWED_ICON_SOURCES:
            errors.append(
                f"icons/manifest.json {ident}: source {source!r} not in allowed set"
            )
        file = item.get("file") or f"{ident}.svg"
        listed.add(file)
        if not (ICONS_DIR / file).is_file():
            errors.append(f"icons/manifest.json lists {file} but the SVG is missing")
    on_disk = {path.name for path in ICONS_DIR.glob("*.svg")}
    for file in sorted(on_disk - listed):
        errors.append(f"icons/{file} has no manifest.json entry")
    return errors


def check_assets(html: str) -> list[str]:
    errors: list[str] = []
    for src in re.findall(r"""src=["'](assets/[^"']+)["']""", html):
        if not (SHOWCASE / src).is_file():
            errors.append(f"index.html src={src!r} is not a file under showcase/")
    return errors


def check_frontmatter(skill: str) -> list[str]:
    errors: list[str] = []
    match = FRONTMATTER.match(skill)
    if not match:
        return ["SKILL.md missing YAML frontmatter"]
    fm, body = match.group(1), match.group(2)
    name_m = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
    desc_m = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
    name = name_m.group(1).strip() if name_m else ""
    desc = desc_m.group(1).strip() if desc_m else ""
    if not NAME_RE.fullmatch(name):
        errors.append(f"SKILL.md name {name!r} must be lowercase-hyphen")
    if len(desc) > 1024:
        errors.append(f"SKILL.md description is {len(desc)} chars (max 1024)")
    if len(body.splitlines()) > 500:
        errors.append(
            f"SKILL.md body is {len(body.splitlines())} lines (max 500)"
        )
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
    match = RAN_TESTS.search(proc.stderr)
    return [f"__ok__ {match.group(0)}"] if match else []


def run_theme_js() -> list[str]:
    node = shutil.which("node")
    if not node:
        return []
    proc = subprocess.run(
        [node, "--test", str(SHOWCASE / "tests" / "test_theme.js")],
        cwd=SHOWCASE,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        return ["showcase/tests/test_theme.js failed:\n" + detail]
    return []


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

    html = INDEX_HTML.read_text(encoding="utf-8")
    if 'data-theme="lights-out"' not in html:
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

    errors.extend(check_frontmatter(skill))
    errors.extend(check_icon_manifest())
    errors.extend(check_assets(html))
    errors.extend(
        check_examples(
            examples,
            SITE_CSS.read_text(encoding="utf-8"),
            html,
        )
    )

    unit = run_unittests()
    ok_line = next((line for line in unit if line.startswith("__ok__")), None)
    errors.extend(line for line in unit if not line.startswith("__ok__"))
    errors.extend(run_theme_js())

    if errors:
        print("\n".join(errors))
        return 1

    print("showcase snapshot OK")
    if ok_line:
        print("unittest:", ok_line.removeprefix("__ok__ "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
