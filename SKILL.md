---
name: wk-x-design-system
description: Applies the pinned X / Twitter design system (tokens, control recipes, and icons from showcase/icons — Heroicons plus an x.com glyph extract from ccrsxx/twitter-clone@62a9588) when building or restyling UI to look like X or Twitter — tweet cards and threads, timelines, composers, Follow / Following, For you / Following tabs, three-column Home, profile cover, hover-card, media grids, lightbox, tooltips, modals (reply, edit profile, username, stats, confirm, mobile sidebar, Display / Customize-your-view, poll composer), loading / error / empty states, lights-out, dim, Grok, Premium, Articles, Communities, Messages / DMs, Notifications, Explore, account switcher — or when the user names this design system, X DS, wk-x-design-system, ccrsxx/twitter-clone, or https://github.com/ccrsxx/twitter-clone. Do not use for unrelated products, generic marketing pages, a copy-only or backend-only task, or a brief that asks for a distinct non-X identity.
---

# wk-x-design-system

Apply the distilled X tokens and control recipes. Do not invent a "Twitter look."

- **Tweet** vs **post**: "Tweet" names clone-era components (matches CSS `.tweet-*`); "post" appears only in x.com-era row names.
- **X** vs **Twitter**: X is the product; Twitter-era names stay where the clone used them (`TwitterIcon`, Tweet CTA).
- **`showcase/`** vs **pin**: `showcase/` is the folder (the catalog of demos); the pin is commit `62a9588`. The x.com extract is a second pin dated 2026-09-16.

## Provenance

Two pinned sources. Both sit in [showcase/](showcase/); neither is re-fetched.

1. **Clone pin** — https://github.com/ccrsxx/twitter-clone at commit `62a9588`: `globals.scss`, `tailwind.config.js`, the Heroicons 2.0.11 glyphs the clone imports (outline, plus solid `CheckBadgeIcon`), its `custom-icon.tsx` glyphs, the two rasters in `showcase/assets/`, and its tweet, input, sidebar, aside, user (profile / hover-card / nav / details), modal, and status components.
2. **x.com extract** — a logged-in x.com session captured 2026-09-16: the glyphs `manifest.json` marks `source: "x.com logged-in extract 2026-09-16"` (`XLogoIcon`, `GrokIcon`, `PremiumIcon`, `ViewsIcon`, and other rail extras) and the current-X patterns (Grok, Premium, Articles, Communities, Messages, Notifications, Explore, Display modal, Poll, topic tabs, account switcher, Today's News, search results / filters, views + bookmark, post detail), rebuilt on the clone's tokens.

Every `data-pattern` in `showcase/` has a row in [examples.md](examples.md); its `Source` column says which era a row belongs to. Use x.com-era patterns and glyphs only when the user asks for current-X chrome or names x.com; otherwise stay on clone-era patterns, and do not mix eras inside one component.

**Source of truth is [showcase/](showcase/)** next to this file — not `twitter-clone` main, not today's x.com, not memory. If the user asks to compare against live x.com, treat the live page as the reference and still write the result with showcase tokens and recipes.

- Do not clone, fetch, or re-distill the GitHub repo, and do not re-extract x.com, unless the user asks to refresh a pin
- Do not vendor Chirp `.woff2`, React, Vite, Tailwind, or Firebase
- Do not `npm install` `@heroicons/react`. Copy SVG from [showcase/icons/](showcase/icons/); `manifest.json` records `source` per icon (`heroicons@2.0.11`, `custom-icon.tsx@62a9588`, or `x.com logged-in extract 2026-09-16`) and `variant` (`outline`, `solid`, `custom`). Do not invent paths
- Rasters: [showcase/assets/](showcase/assets/) holds `no-likes.png` and `twitter-banner.png`, byte-identical to the clone's `public/assets/` at `62a9588`; [showcase/assets/manifest.json](showcase/assets/manifest.json) records source, date, and license. Do not download others

## Resolve the showcase

Read files under `showcase/` beside this `SKILL.md`. Resolve the path from the directory that contains this file; do not assume a home directory or skills root.

- Required: [showcase/tokens.css](showcase/tokens.css), [showcase/site.css](showcase/site.css), [showcase/index.html](showcase/index.html), [showcase/icons/](showcase/icons/)

Task → source → selector: [examples.md](examples.md). Grep `showcase/site.css` for the listed class. Do not read the whole stylesheet unless the selector block is incomplete.

## Defaults

REQUIRED on `html` and in the copied `:root` (paste, do not paraphrase):

```html
<html lang="en" data-theme="lights-out">
```

```css
--main-accent: var(--accent-blue);
```

Copy [showcase/tokens.css](showcase/tokens.css) **verbatim**. Do not reassign `--main-accent` after the copy. Change it only if the user's product brief names yellow, pink, purple, orange, or green. File paths, folder names, branch names, and the word "green" in a test directory are not a brief.

Default logo stays `TwitterIcon` (bird). `XLogoIcon` is the geometric mark for x.com-era chrome, not a logo swap.

- Font: `system-ui, "Segoe UI", sans-serif`
- Body: `16px / 400`, color `var(--text-primary)`, background `rgb(var(--main-background))`
- Motion: `200ms` on color, background, border
- Space: 4px grid. Tweet / composer pad `12px 16px`. Avatar `48px`, gap `12px`. Icon pad `12px`. Follow pad `6px 16px`. Sidebar row gap `16px`, nav icon `28px`, nav label `20px / 700`
- Breakpoints (clone `tailwind.config.js`): `xs 500`, `md 768`, `lg 1024`, `xl 1280`. Sidebar labels only at `≥1280`; icon-only rail `80px` (`96px` from `768`); aside removed `<1024`; `<500` the sidebar becomes a fixed bottom bar and Tweet floats as a Feather disc. Recipes in the `@media` blocks at the end of [showcase/site.css](showcase/site.css)

## Token rules

- RGB-triplet tokens (`--main-background`, `--main-accent`, `--accent-*`) must be used as `rgb(var(--name))` or `rgb(var(--name) / alpha)`
- Hex tokens (`--text-primary`, `--border`, `--twitter-icon`) are used as `var(--name)`
- Theme remaps apply on `html[data-theme="lights-out"|"dim"|"default"]` — do not hard-code page background hex
- Do not add Chirp / TwitterChirp font files or `@font-face` for them
- Do not use `#1DA1F2`, Inter, or Roboto as the "Twitter" stand-in

## Build order

1. Copy [showcase/tokens.css](showcase/tokens.css) verbatim
2. Open the matching row in [examples.md](examples.md)
3. Grep [showcase/site.css](showcase/site.css) for those selectors; reuse class names and values
4. Adapt markup to the product; do not change color, type, radius, or spacing tokens
5. For icons, copy the matching file from [showcase/icons/](showcase/icons/). Tweet actions: `ChatBubbleOvalLeftIcon`, `ArrowPathRoundedSquareIcon`, `HeartIcon`, `ArrowUpTrayIcon` (Heroicons 2.0.11 outline, 20×20, `stroke-width="1.5"`). Views + bookmark (x.com-era `tweet-metrics`) use `ViewsIcon` (filled, x.com extract) and `BookmarkIcon` — don't mix eras inside one action row unless the pattern does
6. Rasters: only `showcase/assets/*.png`, only for the two patterns that use them (`stats-empty`, `auth-landing-clone`). Do not download others
7. Include only the controls the task needs. Do not ship the theme picker or `theme.js` unless the user asked for interactive theme / accent switching
8. Modals, tooltip, hover-card, and lightbox in `showcase/` are static open states. Copy the chrome; wire open / close, focus, and `Escape` in the product's own framework
9. No network, no npm, no Chirp, no Firebase

## Common mistakes

| Rationalization | Do this |
|---|---|
| "I'll pull latest twitter-clone / x.com" | Use `showcase/`: clone pin `62a9588` plus the 2026-09-16 x.com extract. Refresh only if the user asks |
| "Classic Twitter blue is #1DA1F2" | Use `--accent-blue: 29 155 240` (`#1D9BF0`) |
| "Need Chirp to look official" | Distillation dropped Chirp. Use the system stack |
| "I'll freehand a dark card" | Copy `.tweet-card` / `.composer` from `showcase/site.css` |
| "I'll draw reply / like SVGs" | Copy `showcase/icons/*.svg`. Do not invent `d=` |
| "XLogoIcon is in icons/, so I'll use it as the logo" | Keep `TwitterIcon` unless the brief asks for current X |
| "ViewsIcon / GrokIcon are Heroicons" | They are x.com extracts; check `manifest.json` `source` |
| "I'll grab the banner PNG from twitter.com" | Only `showcase/assets/*.png` |
| "This landing page can be X-themed too" | Stop. This skill does not apply |
| "Hex is fine for --main-background" | Keep the RGB triplet; paint with `rgb(var(--main-background))` |

## Red flags

- Any `font-family` other than `system-ui, "Segoe UI", sans-serif`
- Tweet CTA that is not `rgb(var(--main-accent))` with `#ffffff` text, `18px / 700`, pad `12px 32px`, `border-radius: 9999px`
- Follow on lights-out / dim that is not `#EFF3F4` background and `#0F1419` text
- Follow on Default (light) that is not `#0F1419` background and `#ffffff` text
- Following hover that is not `--accent-red` text / fill at `/ 0.1` and border `#F4212E`
- Search focus ring that is not `box-shadow: 0 0 0 2px rgb(var(--main-accent))`
- Selected tab underline that is not `inset 0 -4px 0 rgb(var(--main-accent))`
- `--main-accent` set to anything but `--accent-blue` when the user did not name an accent
- Network fetch of github.com/ccrsxx/twitter-clone or x.com for tokens, patterns, icons, or images — both pins are already in `showcase/`
- Invented SVG `d=` or raster `src` outside `showcase/icons/` and `showcase/assets/`
- `npm install` `@heroicons/react` instead of `showcase/icons/`
- Any `<img src>` that points outside `showcase/assets/`

## Maintaining this skill

After editing `showcase/` or `examples.md`, run `python3 scripts/check_showcase.py`. It pins tokens, cross-checks every `examples.md` row against `site.css` / `index.html`, and runs the Python unittest suite.

`showcase/tests/test_theme.js` needs Node. Run `node --test showcase/tests/test_theme.js` when `node` is on PATH. The checker runs that file when Node is present and skips it — it does not fail — when Node is absent.

`scripts/generate_icons.py` (network fetch) and `scripts/write_offline_icons.py` are maintainer-only, not part of the runtime contract.
