#!/usr/bin/env python3
"""Verify the distilled showcase snapshot still matches the skill contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = SKILL_ROOT / "showcase"
TOKENS = SHOWCASE / "tokens.css"
SKILL_MD = SKILL_ROOT / "SKILL.md"

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
)


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

    for needle in FORBIDDEN_IN_SKILL:
        if needle in skill:
            errors.append(f"SKILL.md still mentions stale path {needle}")

    chirp = list(SHOWCASE.rglob("*chirp*")) + list(SHOWCASE.rglob("*.woff2"))
    if chirp:
        errors.append(f"Chirp/font files in showcase: {chirp}")

    if errors:
        print("\n".join(errors))
        return 1

    print("showcase snapshot OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
