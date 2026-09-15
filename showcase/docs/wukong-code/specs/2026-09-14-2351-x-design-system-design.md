# X Design System Showcase

Date: 2026-09-14 23:51 (UTC+8)  
Source: [ccrsxx/twitter-clone](https://github.com/ccrsxx/twitter-clone) (`62a9588`)  
Status: Approved in conversation (IA, tokens, type/space, controls)

## Problem

X / Twitter did not publish a website design system. `ccrsxx/twitter-clone` is the closest public recreation of that visual language. This project extracts that language into a static showcase people can open in a browser.

## Goal

Ship a single-page static design-system site at `x-design-system/` that maps clone tokens 1:1 and shows the core controls and patterns. Opening `index.html` (or a static file server) is enough. No build step, no npm dependencies, no login, no Firebase.

## Non-goals

- React / Vite / Storybook / Tailwind toolchain
- Real tweet compose, follow, search routing, or any product behavior
- Redistributing Twitter Chirp font files
- Cloning the full app (messages, bookmarks, image upload, Framer Motion)
- Heroicons npm package (use inline SVG instead)
- Tooltip library

## Approach

Static site (Approach A, approved):

| File | Role |
|---|---|
| `index.html` | One page: nav + all sections |
| `tokens.css` | CSS variables (RGB triplets + hex aliases) |
| `site.css` | Showcase chrome and component styles |

Default theme is Lights out (black). A top bar switches 3 backgrounds and 6 accents, matching the clone Display settings.

## Information architecture

Left rail is in-page anchors. Right column is the catalog.

```
+--------------------------------------------------+
|  X DS    [Default|Dim|Lights out]  [6 accents]   |
+----------+---------------------------------------+
| Overview |  Source, how to open, Chirp note      |
| Color    |  Background / text / border / accent / danger |
| Type     |  Scale, weights, underline            |
| Space    |  4px grid, radius, 200ms motion       |
| Controls |  Buttons, follow, search, tab, composer |
| Patterns |  Tweet card, sidebar, menu, avatar, header |
+----------+---------------------------------------+
```

Below `500px` (`xs`, same as the clone): hide the left rail; keep the top theme bar. Sections stack in the same order.

## Theme model

`:root` stores raw RGB triplets. Theme class on `html` remaps semantic aliases.

### Raw backgrounds

| Token | RGB | Hex |
|---|---|---|
| `--dark-background` | `0 0 0` | `#000000` |
| `--dim-background` | `22 33 44` | `#16212C` |
| `--light-background` | `255 255 255` | `#FFFFFF` |
| `--dark-search-background` | `32 35 39` | `#202327` |
| `--dim-search-background` | `39 51 64` | `#273340` |
| `--light-search-background` | `239 243 244` | `#EFF3F4` |
| `--dark-sidebar-background` | `22 24 28` | `#16181C` |
| `--dim-sidebar-background` | `30 39 50` | `#1E2732` |
| `--light-sidebar-background` | `247 249 249` | `#F7F9F9` |

### Semantic aliases (change with theme)

| Token | Default | Dim | Lights out |
|---|---|---|---|
| `--main-background` | light-background | dim-background | dark-background |
| `--main-search-background` | light-search | dim-search | dark-search |
| `--main-sidebar-background` | light-sidebar | dim-sidebar | dark-sidebar |
| `--main-accent` | current accent, default blue | same | same |
| `--text-primary` | `#0F1419` | `#E7E9EA` | `#E7E9EA` |
| `--text-secondary` | `#536471` | `#71767B` | `#71767B` |
| `--border` | `#EFF3F4` | `#2F3336` | `#2F3336` |
| `--reply-line` | `#CFD9DE` | `#333639` | `#333639` |

`--text-primary` / `--text-secondary` are showcase names for the clone pair `light-primary`+`light-secondary` vs `dark-primary`+`dark-secondary`.

### Fixed colors

| Token | RGB | Hex | Use |
|---|---|---|---|
| `--accent-blue` | `29 155 240` | `#1D9BF0` | Default accent |
| `--accent-yellow` | `255 213 0` | `#FFD500` | Accent option |
| `--accent-pink` | `249 26 130` | `#F91A82` | Accent option; like hover |
| `--accent-purple` | `120 87 255` | `#7857FF` | Accent option |
| `--accent-orange` | `255 122 0` | `#FF7A00` | Accent option |
| `--accent-green` | `0 184 122` | `#00B87A` | Accent option; retweet hover |
| `--accent-red` | `244 33 46` | `#F4212E` | Danger / Unfollow |
| `--twitter-icon` | — | `#D6D9DB` | Logo on dark |
| `--image-preview-hover` | — | `#272C30` | Image overlay |

Accent picker sets `--main-accent` to one of the six RGB accents. Theme picker does not reset the accent.

Use `rgb(var(--token) / alpha)` for translucent fills (hover `0.1`, focus ring `0.8`). `--accent-red` is stored as the same RGB triplet (`244 33 46`) so `rgb(var(--accent-red) / 0.1)` works. Hex `#F4212E` is the display label only.

`--reply-line` and `--image-preview-hover` appear as Color swatches only. They are not required on a control in v1.

## Typography

Stack: `system-ui, "Segoe UI", sans-serif`. Do not vendor Chirp `.woff2` files. Overview must state that the clone uses Twitter Chirp (400/500/700/800 + Extended Heavy) and this site uses a system fallback.

| Role | Size | Weight | Clone source |
|---|---|---|---|
| Display | 20px | 700 | Sidebar nav, Home title |
| Title | 18px | 700 | Tweet CTA |
| Body | 16px | 400 | Tweet text (clone leaves body at default) |
| Meta | 14px | 700 | Pinned / Retweeted |
| Secondary | 14px | 400 | Handle, time, helper copy |

Underline: 1px, transparent by default, inherit color on hover and focus-visible.

## Space, radius, motion

4px grid.

| Measure | Value | Where |
|---|---|---|
| Tweet padding | `12px 16px` (top/bottom 12, left/right 16) | Card |
| Avatar-to-text gap | 12px | Card / composer |
| Sidebar item gap | 16px | Nav row |
| Icon button padding | 12px | Clone `p-3` |
| Follow padding | `6px 16px` (top/bottom 6, left/right 16) | Clone `py-1.5 px-4` |
| Nav icon | 28px | Sidebar |
| Default avatar | 48px | Tweet, composer |

| Radius token | Value | Where |
|---|---|---|
| `--radius-full` | 9999px | Buttons, avatar, search |
| `--radius-2xl` | 16px | Modal-shaped surfaces if shown |
| `--radius-md` | 6px | Menu |

Motion: `transition: color, background-color, border-color 200ms`. Accent-filled buttons use `filter: brightness(0.9)` hover and `brightness(0.75)` active. Focus ring 2px: `#878A8C` on light, `#FFFFFF` on dim/lights-out, `rgb(var(--main-accent) / 0.8)` on accent controls. No enter/exit animation.

## Controls

Each control in the catalog shows default / hover / focus / disabled when that state exists, plus the token names.

| Control | Spec |
|---|---|
| Icon button | Circle, 12px pad, hover fill `text-primary / 10` |
| Tweet CTA | Accent fill, white text, 18px/700, brightness hover |
| Follow | Light theme: `#0F1419` fill, white text. Dark/dim: `#EFF3F4` fill, `#0F1419` text. Bold |
| Following | 1px border; hover label becomes "Unfollow", red border, `accent-red / 10` fill |
| Search | Pill, `--main-search-background`; focus: main background + 2px accent ring; magnifier turns accent |
| Tab | Two equal tabs: For you / Following. Active: 4px accent underline, weight 700 |
| Composer | 48px avatar + "What's happening?" in secondary color; Tweet CTA bottom-right, visually disabled |

## Patterns

**Avatar.** 48px circle. Hover `brightness(0.75)`.

**Tweet card.** Padding `12px 16px`, bottom `--border`. Left avatar, right row: name 700 + `@handle` + `·` + time in secondary. Body 16px. Footer four actions (reply / retweet / like / share): idle `--text-secondary`; hover reply/share accent-blue, retweet accent-green, like accent-pink. Hover card fill `3%` black on light, `3%` white on dim/lights-out.

**Sidebar.** Logo (inline X/Twitter bird SVG, dark theme uses `--twitter-icon`, light uses accent-blue). Links: Home, Explore, Notifications, Messages, Bookmarks, Lists, Profile. Active: weight 700, solid icon. Tweet CTA under the list.

**Menu.** `--radius-md`, clone shadow: `#65778633 0 0 15px, #65778626 0 0 3px 1px` on light; `#ffffff33 0 0 15px, #ffffff26 0 0 3px 1px` on dark. Three rows: Delete, Pin to your profile, Bookmark. Row hover 3% black/white.

**Header.** Catalog demo of the clone Home header (not the sticky theme bar). `background: rgb(var(--main-background) / 0.6)` + `backdrop-filter: blur(12px)`. Title "Home" at 20px/700. The theme/accent bar is showcase chrome only.

## Showcase chrome

- Page background `--main-background`, text `--text-primary`.
- Left nav width ~240px; content max-width ~720px (clone main column is about that wide).
- Theme bar is sticky. Switching theme or accent updates CSS variables only; no reload.
- Persist last theme and accent in `localStorage` keys `xds-theme` and `xds-accent` so refresh keeps the choice. Allowed themes: `lights-out` (default), `dim`, `default`. Allowed accents: `blue` (default), `yellow`, `pink`, `purple`, `orange`, `green`.
- Color section: five groups (background, text, border, accent, danger). Each swatch shows color, hex, variable name.
- Sample tweet and sidebar use fixed placeholder copy in English to match the clone UI language.

## Implementation notes

- Vanilla HTML/CSS/JS. One small script for theme/accent + localStorage. No framework.
- Icons: inline SVG, 20–28px stroke/fill as needed. Do not add an icon font.
- Follow / Following are two static examples side by side, not a toggle that hits a backend. Following hover still shows Unfollow (CSS `::before` or a sibling span), matching the clone.
- Composer Tweet button stays disabled.
- `brand/` logos in the parent `others` folder are out of scope; do not copy them in.

## Acceptance

1. Open `index.html` in a browser and see all six sections without a build.
2. Default appearance is Lights out + blue accent.
3. Theme and accent switches recolor the page, including tweet CTA, tab underline, and search focus ring.
4. Token hex values match the tables in this spec (clone source).
5. Viewport below 500px hides the left rail; theme bar remains.
6. No Chirp font files in the repo.
7. No network calls required to render.

## Open-in-browser

Double-click `index.html` or run any static server from `x-design-system/` (for example `python3 -m http.server`). Either is valid.
