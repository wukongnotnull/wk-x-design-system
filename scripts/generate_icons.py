#!/usr/bin/env python3
"""Write distilled 62a9588 icons into showcase/icons/. One-shot snapshot, not a runtime fetch."""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "showcase" / "icons"
HERO_PKG = "https://cdn.jsdelivr.net/npm/heroicons@2.0.11/24"
HERO_JS = "https://cdn.jsdelivr.net/npm/@heroicons/react@2.0.11/24/{set}/esm/{name}.js"

HERO_OUTLINE = [
    "ArchiveBoxXMarkIcon",
    "ArrowLeftIcon",
    "ArrowPathIcon",
    "ArrowPathRoundedSquareIcon",
    "ArrowRightIcon",
    "ArrowRightOnRectangleIcon",
    "ArrowUpRightIcon",
    "ArrowUpTrayIcon",
    "Bars3BottomLeftIcon",
    "BellIcon",
    "BookmarkIcon",
    "BookmarkSlashIcon",
    "CalendarDaysIcon",
    "CameraIcon",
    "ChartBarIcon",
    "ChartPieIcon",
    "ChatBubbleBottomCenterTextIcon",
    "ChatBubbleOvalLeftIcon",
    "CheckIcon",
    "ChevronDownIcon",
    "ChevronRightIcon",
    "Cog8ToothIcon",
    "EllipsisHorizontalCircleIcon",
    "EllipsisHorizontalIcon",
    "EnvelopeIcon",
    "ExclamationTriangleIcon",
    "FaceSmileIcon",
    "GifIcon",
    "GlobeAmericasIcon",
    "HashtagIcon",
    "HeartIcon",
    "HomeIcon",
    "LinkIcon",
    "MagnifyingGlassIcon",
    "MapPinIcon",
    "PaintBrushIcon",
    "PhotoIcon",
    "PlusIcon",
    "QuestionMarkCircleIcon",
    "SparklesIcon",
    "TrashIcon",
    "UserGroupIcon",
    "UserIcon",
    "UserMinusIcon",
    "UserPlusIcon",
    "XMarkIcon",
]

HERO_SOLID = ["CheckBadgeIcon"]


def kebab(name: str) -> str:
    stem = name.removesuffix("Icon")
    parts: list[str] = []
    for i, ch in enumerate(stem):
        prev = stem[i - 1] if i else ""
        if i and ch.isupper() and (prev.islower() or prev.isdigit()):
            parts.append("-")
        elif i and ch.isdigit() and prev.isalpha():
            parts.append("-")
        parts.append(ch.lower())
    return "".join(parts)


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def outline_svg_from_js(name: str, set_name: str) -> str:
    text = fetch(HERO_JS.format(set=set_name, name=name))
    match = re.search(r'd:\s*"([^"]+)"', text)
    if not match:
        raise SystemExit(f"no path in {name} ({set_name})")
    d = match.group(1)
    if set_name == "solid":
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
            'fill="currentColor" aria-hidden="true">\n'
            f'  <path d="{d}"/>\n'
            "</svg>\n"
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" '
        'stroke-width="1.5" stroke="currentColor" aria-hidden="true">\n'
        f'  <path stroke-linecap="round" stroke-linejoin="round" d="{d}"/>\n'
        "</svg>\n"
    )


def try_package_svg(name: str, set_name: str) -> str | None:
    url = f"{HERO_PKG}/{set_name}/{kebab(name)}.svg"
    try:
        return fetch(url)
    except urllib.error.HTTPError:
        return None


CUSTOM = {
    "TwitterIcon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
  <path d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z"/>
</svg>
""",
    "FeatherIcon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
  <path d="M23 3c-6.62-.1-10.38 2.421-13.05 6.03C7.29 12.61 6 17.331 6 22h2c0-1.007.07-2.012.19-3H12c4.1 0 7.48-3.082 7.94-7.054C22.79 10.147 23.17 6.359 23 3zm-7 8h-1.5v2H16c.63-.016 1.2-.08 1.72-.188C16.95 15.24 14.68 17 12 17H8.55c.57-2.512 1.57-4.851 3-6.78 2.16-2.912 5.29-4.911 9.45-5.187C20.95 8.079 19.9 11 16 11zM4 9V6H1V4h3V1h2v3h3v2H6v3H4z"/>
</svg>
""",
    "SpinnerIcon": """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" opacity="0.25"/>
  <path fill="currentColor" opacity="0.75" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
</svg>
""",
    "GoogleIcon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" aria-hidden="true">
  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
  <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
</svg>
""",
    "AppleIcon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
  <path d="M16.365 1.43c0 1.14-.493 2.27-1.177 3.08-.744.9-1.99 1.57-2.987 1.57-.12 0-.23-.02-.3-.03-.01-.06-.04-.22-.04-.39 0-1.15.572-2.27 1.206-2.98.804-.94 2.142-1.64 3.248-1.68.03.13.05.28.05.43zm4.565 15.71c-.03.07-.463 1.58-1.518 3.12-.945 1.34-1.94 2.71-3.43 2.71-1.517 0-1.9-.88-3.63-.88-1.698 0-2.302.91-3.67.91-1.377 0-2.332-1.26-3.428-2.8-1.287-1.82-2.323-4.63-2.323-7.28 0-4.28 2.797-6.55 5.552-6.55 1.448 0 2.675.95 3.6.95.865 0 2.222-1.01 3.902-1.01.613 0 2.886.06 4.374 2.19-.13.09-2.383 1.37-2.383 4.19 0 3.26 2.854 4.42 2.955 4.45z"/>
</svg>
""",
    "TriangleIcon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
  <path d="M12.538 6.478c-.14-.146-.335-.228-.538-.228s-.396.082-.538.228l-9.252 9.53c-.21.217-.27.538-.152.815.117.277.39.458.69.458h18.5c.302 0 .573-.18.69-.457.118-.277.058-.598-.152-.814l-9.248-9.532z"/>
</svg>
""",
    "PinIcon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M15 4.5l-4 4l-4 1.5l-1.5 1.5l7 7l1.5 -1.5l1.5 -4l4 -4"/>
  <line x1="9" y1="15" x2="4.5" y2="19.5"/>
  <line x1="14.5" y1="4" x2="20" y2="9.5"/>
</svg>
""",
    "PinOffIcon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <line x1="3" y1="3" x2="21" y2="21"/>
  <path d="M15 4.5l-3.249 3.249m-2.57 1.433l-2.181 .818l-1.5 1.5l7 7l1.5 -1.5l.82 -2.186m1.43 -2.563l3.25 -3.251"/>
  <line x1="9" y1="15" x2="4.5" y2="19.5"/>
  <line x1="14.5" y1="4" x2="20" y2="9.5"/>
</svg>
""",
}


def write_icon(name: str, svg: str, source: str, variant: str, items: list[dict]) -> None:
    (OUT / f"{name}.svg").write_text(svg if svg.endswith("\n") else svg + "\n", encoding="utf-8")
    items.append({"id": name, "source": source, "variant": variant, "file": f"{name}.svg"})


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    items: list[dict] = []

    for name in HERO_OUTLINE:
        svg = try_package_svg(name, "outline") or outline_svg_from_js(name, "outline")
        write_icon(name, svg, "heroicons@2.0.11", "outline", items)

    for name in HERO_SOLID:
        svg = try_package_svg(name, "solid") or outline_svg_from_js(name, "solid")
        write_icon(name, svg, "heroicons@2.0.11", "solid", items)

    for name, svg in CUSTOM.items():
        write_icon(name, svg, "custom-icon.tsx@62a9588", "custom", items)

    items.sort(key=lambda row: row["id"])
    manifest = {
        "commit": "62a9588",
        "repo": "ccrsxx/twitter-clone",
        "heroicons": "@heroicons/react@2.0.11",
        "icons": items,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(items)} icons to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
