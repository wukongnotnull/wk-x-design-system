# X Design System Showcase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use wukong-code:subagent-driven-development (recommended) or wukong-code:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a static single-page design-system showcase that maps `ccrsxx/twitter-clone` tokens 1:1 and shows the approved controls and patterns.

**Architecture:** Three runtime files (`tokens.css`, `site.css`, `index.html`) plus one script (`theme.js`) that remaps CSS variables on `html` and persists theme/accent in `localStorage`. Python and Node stdlib tests lock token values and file contracts. No bundler, no npm package.

**Tech Stack:** HTML, CSS custom properties, vanilla JS, Python 3 `unittest`, Node.js `node:test` (stdlib only).

## Global Constraints

- No build step, no npm dependencies, no login, no Firebase.
- Do not vendor Chirp `.woff` / `.woff2` files; font stack is `system-ui, "Segoe UI", sans-serif`.
- No network calls required to render.
- Icons are inline SVG only; no icon font and no Heroicons package.
- `localStorage` keys: `xds-theme`, `xds-accent`.
- Allowed themes: `lights-out` (default), `dim`, `default`.
- Allowed accents: `blue` (default), `yellow`, `pink`, `purple`, `orange`, `green`.
- Default appearance: Lights out + blue accent.
- Breakpoint `xs = 500px`: hide left rail, keep sticky theme bar.
- Do not copy files from parent `others/brand/`.
- Follow / Following are static side-by-side examples; composer Tweet button stays disabled.
- Sample copy is English.

## File Structure

| File | Responsibility |
|---|---|
| `tokens.css` | Raw RGB triplets, hex labels as comments, semantic aliases per `html[data-theme]` |
| `theme.js` | `applyTheme`, `applyAccent`, `persist`, `loadPersisted`, `boot` |
| `site.css` | Showcase chrome and every catalog component |
| `index.html` | One page: theme bar, left nav, six sections |
| `tests/test_tokens.py` | Token RGB/hex contract |
| `tests/test_theme.js` | Theme/accent API + persistence |
| `tests/test_html.py` | Section ids, controls, patterns, no Chirp, no fetch |

---

### Task 1: Token stylesheet

**Files:**
- Create: `tests/test_tokens.py`
- Create: `tokens.css`

**Interfaces:**
- Consumes: nothing
- Produces: `tokens.css` with `:root` raw tokens and `html[data-theme="lights-out"|"dim"|"default"]` semantic aliases. Theme script later only sets `data-theme` and `--main-accent`.

- [ ] **Step 1: Write the failing test**

```python
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "tokens.css").read_text(encoding="utf-8")


def decl(name: str) -> str:
    match = re.search(rf"{re.escape(name)}:\s*([^;]+);", CSS)
    if not match:
        raise AssertionError(f"missing {name}")
    return re.sub(r"\s+", " ", match.group(1).strip())


class TokenContractTest(unittest.TestCase):
    def test_raw_background_triplets(self):
        self.assertEqual(decl("--dark-background"), "0 0 0")
        self.assertEqual(decl("--dim-background"), "22 33 44")
        self.assertEqual(decl("--light-background"), "255 255 255")
        self.assertEqual(decl("--dark-search-background"), "32 35 39")
        self.assertEqual(decl("--dim-search-background"), "39 51 64")
        self.assertEqual(decl("--light-search-background"), "239 243 244")
        self.assertEqual(decl("--dark-sidebar-background"), "22 24 28")
        self.assertEqual(decl("--dim-sidebar-background"), "30 39 50")
        self.assertEqual(decl("--light-sidebar-background"), "247 249 249")

    def test_fixed_accent_triplets(self):
        self.assertEqual(decl("--accent-blue"), "29 155 240")
        self.assertEqual(decl("--accent-yellow"), "255 213 0")
        self.assertEqual(decl("--accent-pink"), "249 26 130")
        self.assertEqual(decl("--accent-purple"), "120 87 255")
        self.assertEqual(decl("--accent-orange"), "255 122 0")
        self.assertEqual(decl("--accent-green"), "0 184 122")
        self.assertEqual(decl("--accent-red"), "244 33 46")

    def test_hex_only_tokens(self):
        self.assertEqual(decl("--twitter-icon"), "#D6D9DB")
        self.assertEqual(decl("--image-preview-hover"), "#272C30")

    def test_radius_tokens(self):
        self.assertEqual(decl("--radius-full"), "9999px")
        self.assertEqual(decl("--radius-2xl"), "16px")
        self.assertEqual(decl("--radius-md"), "6px")

    def test_default_semantic_on_root(self):
        self.assertIn('data-theme="lights-out"', CSS)
        self.assertEqual(decl("--main-accent"), "var(--accent-blue)")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_tokens.py -v`

Expected: FAIL with `FileNotFoundError` or missing `--dark-background`.

- [ ] **Step 3: Write minimal implementation**

Create `tokens.css`:

```css
:root {
  --dark-background: 0 0 0;
  --dim-background: 22 33 44;
  --light-background: 255 255 255;
  --dark-search-background: 32 35 39;
  --dim-search-background: 39 51 64;
  --light-search-background: 239 243 244;
  --dark-sidebar-background: 22 24 28;
  --dim-sidebar-background: 30 39 50;
  --light-sidebar-background: 247 249 249;

  --accent-yellow: 255 213 0;
  --accent-blue: 29 155 240;
  --accent-pink: 249 26 130;
  --accent-purple: 120 87 255;
  --accent-orange: 255 122 0;
  --accent-green: 0 184 122;
  --accent-red: 244 33 46;

  --twitter-icon: #D6D9DB;
  --image-preview-hover: #272C30;

  --text-light-primary: #0F1419;
  --text-light-secondary: #536471;
  --text-dark-primary: #E7E9EA;
  --text-dark-secondary: #71767B;
  --border-light: #EFF3F4;
  --border-dark: #2F3336;
  --reply-line-light: #CFD9DE;
  --reply-line-dark: #333639;

  --radius-full: 9999px;
  --radius-2xl: 16px;
  --radius-md: 6px;

  --main-accent: var(--accent-blue);
}

html[data-theme="lights-out"] {
  --main-background: var(--dark-background);
  --main-search-background: var(--dark-search-background);
  --main-sidebar-background: var(--dark-sidebar-background);
  --text-primary: var(--text-dark-primary);
  --text-secondary: var(--text-dark-secondary);
  --border: var(--border-dark);
  --reply-line: var(--reply-line-dark);
}

html[data-theme="dim"] {
  --main-background: var(--dim-background);
  --main-search-background: var(--dim-search-background);
  --main-sidebar-background: var(--dim-sidebar-background);
  --text-primary: var(--text-dark-primary);
  --text-secondary: var(--text-dark-secondary);
  --border: var(--border-dark);
  --reply-line: var(--reply-line-dark);
}

html[data-theme="default"] {
  --main-background: var(--light-background);
  --main-search-background: var(--light-search-background);
  --main-sidebar-background: var(--light-sidebar-background);
  --text-primary: var(--text-light-primary);
  --text-secondary: var(--text-light-secondary);
  --border: var(--border-light);
  --reply-line: var(--reply-line-light);
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_tokens.py -v`

Expected: PASS (5 tests).

- [ ] **Step 5: Commit**

```bash
git add tests/test_tokens.py tokens.css
git commit -m "feat: add clone-accurate CSS tokens"
```

---

### Task 2: Theme and accent script

**Files:**
- Create: `tests/test_theme.js`
- Create: `theme.js`

**Interfaces:**
- Consumes: `tokens.css` semantic aliases (`html[data-theme]`, `--main-accent`)
- Produces:
  - `THEMES = ["lights-out", "dim", "default"]`
  - `ACCENTS = { blue, yellow, pink, purple, orange, green }` mapped to `var(--accent-*)`
  - `applyTheme(root, theme) => string` — sets `data-theme`, falls back to `lights-out`
  - `applyAccent(root, accent) => string` — sets `--main-accent`, falls back to `blue`
  - `persist(storage, theme, accent) => void` — writes `xds-theme` and `xds-accent`
  - `loadPersisted(storage) => { theme: string, accent: string }`
  - `boot(root, storage) => { theme: string, accent: string }` — load, apply, persist defaults

- [ ] **Step 1: Write the failing test**

```js
const test = require("node:test");
const assert = require("node:assert/strict");
const { applyTheme, applyAccent, persist, loadPersisted, boot } = require("../theme.js");

function fakeRoot() {
  const styles = {};
  return {
    dataset: {},
    style: {
      setProperty(name, value) {
        styles[name] = value;
      },
      getPropertyValue(name) {
        return styles[name] || "";
      }
    }
  };
}

function fakeStorage(initial) {
  const data = { ...initial };
  return {
    getItem(key) {
      return Object.prototype.hasOwnProperty.call(data, key) ? data[key] : null;
    },
    setItem(key, value) {
      data[key] = String(value);
    },
    _data: data
  };
}

test("applyTheme sets data-theme and rejects unknown values", () => {
  const root = fakeRoot();
  assert.equal(applyTheme(root, "dim"), "dim");
  assert.equal(root.dataset.theme, "dim");
  assert.equal(applyTheme(root, "nope"), "lights-out");
  assert.equal(root.dataset.theme, "lights-out");
});

test("applyAccent sets --main-accent CSS variable", () => {
  const root = fakeRoot();
  assert.equal(applyAccent(root, "pink"), "pink");
  assert.equal(root.style.getPropertyValue("--main-accent"), "var(--accent-pink)");
  assert.equal(applyAccent(root, "nope"), "blue");
  assert.equal(root.style.getPropertyValue("--main-accent"), "var(--accent-blue)");
});

test("persist and loadPersisted use xds-theme and xds-accent", () => {
  const storage = fakeStorage({});
  persist(storage, "default", "green");
  assert.deepEqual(loadPersisted(storage), { theme: "default", accent: "green" });
});

test("boot defaults to lights-out and blue when storage is empty", () => {
  const root = fakeRoot();
  const storage = fakeStorage({});
  const result = boot(root, storage);
  assert.deepEqual(result, { theme: "lights-out", accent: "blue" });
  assert.equal(root.dataset.theme, "lights-out");
  assert.equal(root.style.getPropertyValue("--main-accent"), "var(--accent-blue)");
  assert.equal(storage.getItem("xds-theme"), "lights-out");
  assert.equal(storage.getItem("xds-accent"), "blue");
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/test_theme.js`

Expected: FAIL with `Cannot find module '../theme.js'`.

- [ ] **Step 3: Write minimal implementation**

Create `theme.js`:

```js
const THEMES = ["lights-out", "dim", "default"];
const ACCENTS = {
  blue: "var(--accent-blue)",
  yellow: "var(--accent-yellow)",
  pink: "var(--accent-pink)",
  purple: "var(--accent-purple)",
  orange: "var(--accent-orange)",
  green: "var(--accent-green)"
};

function applyTheme(root, theme) {
  const next = THEMES.includes(theme) ? theme : "lights-out";
  root.dataset.theme = next;
  return next;
}

function applyAccent(root, accent) {
  const next = ACCENTS[accent] ? accent : "blue";
  root.style.setProperty("--main-accent", ACCENTS[next]);
  return next;
}

function persist(storage, theme, accent) {
  storage.setItem("xds-theme", theme);
  storage.setItem("xds-accent", accent);
}

function loadPersisted(storage) {
  return {
    theme: storage.getItem("xds-theme") || "lights-out",
    accent: storage.getItem("xds-accent") || "blue"
  };
}

function boot(root, storage) {
  const loaded = loadPersisted(storage);
  const theme = applyTheme(root, loaded.theme);
  const accent = applyAccent(root, loaded.accent);
  persist(storage, theme, accent);
  return { theme, accent };
}

function onReady() {
  const root = document.documentElement;
  const storage = window.localStorage;
  boot(root, storage);

  document.querySelectorAll("[data-set-theme]").forEach((button) => {
    button.addEventListener("click", () => {
      const theme = applyTheme(root, button.getAttribute("data-set-theme"));
      persist(storage, theme, loadPersisted(storage).accent);
    });
  });

  document.querySelectorAll("[data-set-accent]").forEach((button) => {
    button.addEventListener("click", () => {
      const accent = applyAccent(root, button.getAttribute("data-set-accent"));
      persist(storage, loadPersisted(storage).theme, accent);
    });
  });
}

if (typeof document !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
}

const api = {
  THEMES,
  ACCENTS,
  applyTheme,
  applyAccent,
  persist,
  loadPersisted,
  boot
};

if (typeof module === "object" && module.exports) {
  module.exports = api;
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test tests/test_theme.js`

Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add tests/test_theme.js theme.js
git commit -m "feat: persist theme and accent on the document root"
```

---

### Task 3: Page chrome and six section shells

**Files:**
- Create: `tests/test_html.py`
- Create: `site.css`
- Create: `index.html`

**Interfaces:**
- Consumes: `tokens.css`; `theme.js` `boot` + `[data-set-theme]` / `[data-set-accent]`
- Produces: `index.html` with `html data-theme="lights-out"`, sticky `#theme-bar`, `#rail` links, and section ids `overview`, `color`, `type`, `space`, `controls`, `patterns`. `site.css` hides `#rail` below 500px.

- [ ] **Step 1: Write the failing test**

```python
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
SITE = (ROOT / "site.css").read_text(encoding="utf-8")


class HtmlChromeTest(unittest.TestCase):
    def test_default_theme_attribute(self):
        self.assertIn('data-theme="lights-out"', HTML)

    def test_styles_and_script_linked(self):
        self.assertIn('href="tokens.css"', HTML)
        self.assertIn('href="site.css"', HTML)
        self.assertIn('src="theme.js"', HTML)

    def test_section_ids(self):
        for section_id in ("overview", "color", "type", "space", "controls", "patterns"):
            self.assertIn(f'id="{section_id}"', HTML)

    def test_theme_and_accent_buttons(self):
        for theme in ("lights-out", "dim", "default"):
            self.assertIn(f'data-set-theme="{theme}"', HTML)
        for accent in ("blue", "yellow", "pink", "purple", "orange", "green"):
            self.assertIn(f'data-set-accent="{accent}"', HTML)

    def test_rail_hidden_below_500px(self):
        self.assertIn("@media (max-width: 499px)", SITE)
        self.assertIn("#rail", SITE)

    def test_overview_mentions_chirp_fallback(self):
        self.assertIn("Chirp", HTML)
        self.assertIn("system-ui", HTML)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_html.py -v`

Expected: FAIL with `FileNotFoundError` for `index.html`.

- [ ] **Step 3: Write minimal implementation**

Create `site.css`:

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  min-height: 100%;
}

body {
  font-family: system-ui, "Segoe UI", sans-serif;
  font-size: 16px;
  font-weight: 400;
  color: var(--text-primary);
  background: rgb(var(--main-background));
  transition: color 200ms, background-color 200ms, border-color 200ms;
}

a {
  color: inherit;
}

#theme-bar {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  background: rgb(var(--main-background) / 0.6);
  backdrop-filter: blur(12px);
}

#theme-bar .brand {
  font-size: 20px;
  font-weight: 700;
  margin-right: 8px;
}

.picker {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.picker button {
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-primary);
  border-radius: var(--radius-full);
  padding: 6px 12px;
  cursor: pointer;
  transition: color 200ms, background-color 200ms, border-color 200ms;
}

.picker button:hover {
  background: rgb(var(--text-primary-rgb, 231 233 234) / 0.1);
}

html[data-theme="default"] .picker button:hover {
  background: rgb(15 20 25 / 0.1);
}

html[data-theme="lights-out"] .picker button:hover,
html[data-theme="dim"] .picker button:hover {
  background: rgb(231 233 234 / 0.1);
}

.layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 720px);
  gap: 24px;
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px 16px 80px;
}

#rail {
  position: sticky;
  top: 72px;
  align-self: start;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

#rail a {
  text-decoration: none;
  padding: 8px 12px;
  border-radius: var(--radius-full);
}

#rail a:hover {
  background: rgb(231 233 234 / 0.1);
}

html[data-theme="default"] #rail a:hover {
  background: rgb(15 20 25 / 0.1);
}

main section {
  margin-bottom: 48px;
}

main h1,
main h2 {
  font-size: 20px;
  font-weight: 700;
}

@media (max-width: 499px) {
  #rail {
    display: none;
  }

  .layout {
    grid-template-columns: 1fr;
  }
}
```

Create `index.html`:

```html
<!DOCTYPE html>
<html lang="en" data-theme="lights-out">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>X Design System</title>
    <link rel="stylesheet" href="tokens.css" />
    <link rel="stylesheet" href="site.css" />
  </head>
  <body>
    <header id="theme-bar">
      <span class="brand">X DS</span>
      <div class="picker" aria-label="Background theme">
        <button type="button" data-set-theme="default">Default</button>
        <button type="button" data-set-theme="dim">Dim</button>
        <button type="button" data-set-theme="lights-out">Lights out</button>
      </div>
      <div class="picker" aria-label="Accent color">
        <button type="button" data-set-accent="blue">Blue</button>
        <button type="button" data-set-accent="yellow">Yellow</button>
        <button type="button" data-set-accent="pink">Pink</button>
        <button type="button" data-set-accent="purple">Purple</button>
        <button type="button" data-set-accent="orange">Orange</button>
        <button type="button" data-set-accent="green">Green</button>
      </div>
    </header>
    <div class="layout">
      <nav id="rail">
        <a href="#overview">Overview</a>
        <a href="#color">Color</a>
        <a href="#type">Type</a>
        <a href="#space">Space</a>
        <a href="#controls">Controls</a>
        <a href="#patterns">Patterns</a>
      </nav>
      <main>
        <section id="overview">
          <h1>Overview</h1>
          <p>
            Tokens and components extracted from
            <a class="text-link" href="https://github.com/ccrsxx/twitter-clone">ccrsxx/twitter-clone</a>.
            Open this file directly or run <code>python3 -m http.server</code> from this folder.
          </p>
          <p>
            The clone ships Twitter Chirp (400 / 500 / 700 / 800 and Extended Heavy).
            This showcase does not redistribute those files and uses
            <code>system-ui, "Segoe UI", sans-serif</code> instead.
          </p>
        </section>
        <section id="color"><h2>Color</h2></section>
        <section id="type"><h2>Type</h2></section>
        <section id="space"><h2>Space</h2></section>
        <section id="controls"><h2>Controls</h2></section>
        <section id="patterns"><h2>Patterns</h2></section>
      </main>
    </div>
    <script src="theme.js"></script>
  </body>
</html>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_html.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_html.py site.css index.html
git commit -m "feat: add showcase chrome and section shells"
```

---

### Task 4: Color catalog

**Files:**
- Modify: `tests/test_html.py`
- Modify: `site.css`
- Modify: `index.html` (`#color` only)

**Interfaces:**
- Consumes: token names from Task 1
- Produces: five groups in `#color` — `background`, `text`, `border`, `accent`, `danger` — each swatch has `data-token`, hex text, and variable name

- [ ] **Step 1: Write the failing test**

Append to `HtmlChromeTest` in `tests/test_html.py`:

```python
    def test_color_groups_and_swatches(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for group in ("background", "text", "border", "accent", "danger"):
            self.assertIn(f'data-color-group="{group}"', html)
        for token in (
            "--main-background",
            "--main-search-background",
            "--main-sidebar-background",
            "--text-primary",
            "--text-secondary",
            "--border",
            "--reply-line",
            "--accent-blue",
            "--accent-yellow",
            "--accent-pink",
            "--accent-purple",
            "--accent-orange",
            "--accent-green",
            "--accent-red",
            "--twitter-icon",
            "--image-preview-hover",
        ):
            self.assertIn(f'data-token="{token}"', html)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_html.HtmlChromeTest.test_color_groups_and_swatches -v`

Expected: FAIL (`data-color-group` missing).

- [ ] **Step 3: Write minimal implementation**

Append to `site.css`:

```css
.swatch-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.swatch {
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}

.swatch-chip {
  height: 72px;
}

.swatch figcaption {
  padding: 8px 12px;
  font-size: 14px;
  color: var(--text-secondary);
}

.swatch code {
  display: block;
  color: var(--text-primary);
}

.group-title {
  font-size: 14px;
  font-weight: 700;
  margin: 24px 0 12px;
}
```

Replace the empty `#color` section in `index.html` with:

```html
        <section id="color">
          <h2>Color</h2>
          <h3 class="group-title">Background</h3>
          <div class="swatch-grid" data-color-group="background">
            <figure class="swatch" data-token="--main-background">
              <div class="swatch-chip" style="background: rgb(var(--main-background))"></div>
              <figcaption><code>--main-background</code> theme surface</figcaption>
            </figure>
            <figure class="swatch" data-token="--main-search-background">
              <div class="swatch-chip" style="background: rgb(var(--main-search-background))"></div>
              <figcaption><code>--main-search-background</code> #202327 / #273340 / #EFF3F4</figcaption>
            </figure>
            <figure class="swatch" data-token="--main-sidebar-background">
              <div class="swatch-chip" style="background: rgb(var(--main-sidebar-background))"></div>
              <figcaption><code>--main-sidebar-background</code> #16181C / #1E2732 / #F7F9F9</figcaption>
            </figure>
          </div>
          <h3 class="group-title">Text</h3>
          <div class="swatch-grid" data-color-group="text">
            <figure class="swatch" data-token="--text-primary">
              <div class="swatch-chip" style="background: var(--text-primary)"></div>
              <figcaption><code>--text-primary</code> #E7E9EA / #0F1419</figcaption>
            </figure>
            <figure class="swatch" data-token="--text-secondary">
              <div class="swatch-chip" style="background: var(--text-secondary)"></div>
              <figcaption><code>--text-secondary</code> #71767B / #536471</figcaption>
            </figure>
          </div>
          <h3 class="group-title">Border</h3>
          <div class="swatch-grid" data-color-group="border">
            <figure class="swatch" data-token="--border">
              <div class="swatch-chip" style="background: var(--border)"></div>
              <figcaption><code>--border</code> #2F3336 / #EFF3F4</figcaption>
            </figure>
            <figure class="swatch" data-token="--reply-line">
              <div class="swatch-chip" style="background: var(--reply-line)"></div>
              <figcaption><code>--reply-line</code> #333639 / #CFD9DE</figcaption>
            </figure>
          </div>
          <h3 class="group-title">Accent</h3>
          <div class="swatch-grid" data-color-group="accent">
            <figure class="swatch" data-token="--accent-blue">
              <div class="swatch-chip" style="background: rgb(var(--accent-blue))"></div>
              <figcaption><code>--accent-blue</code> #1D9BF0</figcaption>
            </figure>
            <figure class="swatch" data-token="--accent-yellow">
              <div class="swatch-chip" style="background: rgb(var(--accent-yellow))"></div>
              <figcaption><code>--accent-yellow</code> #FFD500</figcaption>
            </figure>
            <figure class="swatch" data-token="--accent-pink">
              <div class="swatch-chip" style="background: rgb(var(--accent-pink))"></div>
              <figcaption><code>--accent-pink</code> #F91A82</figcaption>
            </figure>
            <figure class="swatch" data-token="--accent-purple">
              <div class="swatch-chip" style="background: rgb(var(--accent-purple))"></div>
              <figcaption><code>--accent-purple</code> #7857FF</figcaption>
            </figure>
            <figure class="swatch" data-token="--accent-orange">
              <div class="swatch-chip" style="background: rgb(var(--accent-orange))"></div>
              <figcaption><code>--accent-orange</code> #FF7A00</figcaption>
            </figure>
            <figure class="swatch" data-token="--accent-green">
              <div class="swatch-chip" style="background: rgb(var(--accent-green))"></div>
              <figcaption><code>--accent-green</code> #00B87A</figcaption>
            </figure>
            <figure class="swatch" data-token="--twitter-icon">
              <div class="swatch-chip" style="background: var(--twitter-icon)"></div>
              <figcaption><code>--twitter-icon</code> #D6D9DB</figcaption>
            </figure>
            <figure class="swatch" data-token="--image-preview-hover">
              <div class="swatch-chip" style="background: var(--image-preview-hover)"></div>
              <figcaption><code>--image-preview-hover</code> #272C30</figcaption>
            </figure>
          </div>
          <h3 class="group-title">Danger</h3>
          <div class="swatch-grid" data-color-group="danger">
            <figure class="swatch" data-token="--accent-red">
              <div class="swatch-chip" style="background: rgb(var(--accent-red))"></div>
              <figcaption><code>--accent-red</code> #F4212E</figcaption>
            </figure>
          </div>
        </section>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_html.HtmlChromeTest.test_color_groups_and_swatches -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_html.py site.css index.html
git commit -m "feat: add color token catalog"
```

---

### Task 5: Type and space catalog

**Files:**
- Modify: `tests/test_html.py`
- Modify: `site.css`
- Modify: `index.html` (`#type` and `#space`)

**Interfaces:**
- Consumes: type roles and radius tokens from the spec
- Produces: five type specimens (`display`, `title`, `body`, `meta`, `secondary`) and space samples for padding, radius, and 200ms motion

- [ ] **Step 1: Write the failing test**

Append to `HtmlChromeTest`:

```python
    def test_type_roles(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for role in ("display", "title", "body", "meta", "secondary"):
            self.assertIn(f'data-type="{role}"', html)
        self.assertIn("custom-underline", html)

    def test_space_tokens(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn("12px 16px", html)
        self.assertIn("200ms", css)
        self.assertIn("var(--radius-full)", css)
        self.assertIn("var(--radius-2xl)", css)
        self.assertIn("var(--radius-md)", css)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_html.HtmlChromeTest.test_type_roles tests.test_html.HtmlChromeTest.test_space_tokens -v`

Expected: FAIL (`data-type` missing).

- [ ] **Step 3: Write minimal implementation**

Append to `site.css`:

```css
.type-display {
  font-size: 20px;
  font-weight: 700;
}

.type-title {
  font-size: 18px;
  font-weight: 700;
}

.type-body {
  font-size: 16px;
  font-weight: 400;
}

.type-meta {
  font-size: 14px;
  font-weight: 700;
}

.type-secondary {
  font-size: 14px;
  font-weight: 400;
  color: var(--text-secondary);
}

.custom-underline {
  text-decoration: underline;
  text-decoration-color: transparent;
  text-decoration-thickness: 1px;
  transition: color 200ms, background-color 200ms, border-color 200ms, text-decoration-color 200ms;
}

.custom-underline:hover,
.custom-underline:focus-visible {
  text-decoration-color: inherit;
}

.space-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: end;
}

.space-box {
  border: 1px dashed var(--border);
}

.radius-demo {
  width: 64px;
  height: 64px;
  background: rgb(var(--main-accent));
}

.motion-demo {
  padding: 12px 16px;
  border-radius: var(--radius-full);
  background: rgb(var(--main-sidebar-background));
  transition: color 200ms, background-color 200ms, border-color 200ms;
}

.motion-demo:hover {
  background: rgb(var(--main-accent) / 0.1);
  color: rgb(var(--main-accent));
}
```

Replace `#type` and `#space` in `index.html` with:

```html
        <section id="type">
          <h2>Type</h2>
          <p class="type-display" data-type="display">Display 20 / 700 — Home, sidebar</p>
          <p class="type-title" data-type="title">Title 18 / 700 — Tweet CTA</p>
          <p class="type-body" data-type="body">Body 16 / 400 — tweet text</p>
          <p class="type-meta" data-type="meta">Meta 14 / 700 — Pinned Tweet</p>
          <p class="type-secondary" data-type="secondary">Secondary 14 / 400 — @handle · 2h</p>
          <p><a class="custom-underline" href="#type">Underline hover / focus</a></p>
        </section>
        <section id="space">
          <h2>Space</h2>
          <p>4px grid. Tweet padding <code>12px 16px</code>. Avatar gap 12px. Icon pad 12px. Follow pad <code>6px 16px</code>.</p>
          <div class="space-row">
            <div class="space-box" style="padding: 12px 16px">12×16</div>
            <div class="radius-demo" style="border-radius: var(--radius-full)" title="--radius-full"></div>
            <div class="radius-demo" style="border-radius: var(--radius-2xl)" title="--radius-2xl"></div>
            <div class="radius-demo" style="border-radius: var(--radius-md)" title="--radius-md"></div>
            <button type="button" class="motion-demo">200ms hover</button>
          </div>
        </section>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_html.HtmlChromeTest.test_type_roles tests.test_html.HtmlChromeTest.test_space_tokens -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_html.py site.css index.html
git commit -m "feat: add type and space specimens"
```

---

### Task 6: Controls catalog

**Files:**
- Modify: `tests/test_html.py`
- Modify: `site.css`
- Modify: `index.html` (`#controls`)

**Interfaces:**
- Consumes: `--main-accent`, `--accent-red`, `--text-primary`, radius-full
- Produces: static demos with `data-control` values `icon`, `tweet-cta`, `follow`, `following`, `search`, `tab`, `composer`

- [ ] **Step 1: Write the failing test**

Append to `HtmlChromeTest`:

```python
    def test_controls(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for control in ("icon", "tweet-cta", "follow", "following", "search", "tab", "composer"):
            self.assertIn(f'data-control="{control}"', html)
        self.assertIn("What's happening?", html)
        self.assertIn('disabled', html)
        self.assertIn("For you", html)
        self.assertIn("Following", html)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_html.HtmlChromeTest.test_controls -v`

Expected: FAIL (`data-control` missing).

- [ ] **Step 3: Write minimal implementation**

Append to `site.css`:

```css
.catalog-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
  margin: 16px 0;
}

.icon-button {
  width: 48px;
  height: 48px;
  padding: 12px;
  border: 0;
  border-radius: var(--radius-full);
  background: transparent;
  color: var(--text-primary);
  cursor: pointer;
  transition: color 200ms, background-color 200ms, border-color 200ms;
}

.icon-button:hover {
  background: rgb(231 233 234 / 0.1);
}

html[data-theme="default"] .icon-button:hover {
  background: rgb(15 20 25 / 0.1);
}

.icon-button:focus-visible {
  outline: 2px solid #878A8C;
  outline-offset: 2px;
}

html[data-theme="lights-out"] .icon-button:focus-visible,
html[data-theme="dim"] .icon-button:focus-visible {
  outline-color: #ffffff;
}

.tweet-cta {
  border: 0;
  border-radius: var(--radius-full);
  padding: 12px 32px;
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
  background: rgb(var(--main-accent));
  cursor: pointer;
  transition: color 200ms, background-color 200ms, border-color 200ms, filter 200ms;
}

.tweet-cta:hover {
  filter: brightness(0.9);
}

.tweet-cta:active {
  filter: brightness(0.75);
}

.tweet-cta:focus-visible {
  outline: 2px solid rgb(var(--main-accent) / 0.8);
  outline-offset: 2px;
}

.tweet-cta:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: none;
}

.btn-follow {
  border: 0;
  border-radius: var(--radius-full);
  padding: 6px 16px;
  min-width: 106px;
  font-weight: 700;
  cursor: pointer;
  background: #0F1419;
  color: #ffffff;
  transition: color 200ms, background-color 200ms, border-color 200ms;
}

html[data-theme="lights-out"] .btn-follow,
html[data-theme="dim"] .btn-follow {
  background: #EFF3F4;
  color: #0F1419;
}

.btn-following {
  position: relative;
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  padding: 6px 16px;
  min-width: 106px;
  font-weight: 700;
  cursor: pointer;
  background: transparent;
  color: var(--text-primary);
  transition: color 200ms, background-color 200ms, border-color 200ms;
}

.btn-following .idle {
  display: inline;
}

.btn-following .hover {
  display: none;
}

.btn-following:hover {
  border-color: #F4212E;
  background: rgb(var(--accent-red) / 0.1);
  color: rgb(var(--accent-red));
}

.btn-following:hover .idle {
  display: none;
}

.btn-following:hover .hover {
  display: inline;
}

.search {
  display: flex;
  align-items: center;
  gap: 12px;
  width: min(100%, 360px);
  padding: 8px 16px;
  border-radius: var(--radius-full);
  background: rgb(var(--main-search-background));
  transition: color 200ms, background-color 200ms, border-color 200ms, box-shadow 200ms;
}

.search:focus-within {
  background: rgb(var(--main-background));
  box-shadow: 0 0 0 2px rgb(var(--main-accent));
}

.search:focus-within svg {
  color: rgb(var(--main-accent));
}

.search input {
  flex: 1;
  border: 0;
  background: transparent;
  color: var(--text-primary);
  outline: none;
  font: inherit;
}

.search input::placeholder {
  color: var(--text-secondary);
}

.tabs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-bottom: 1px solid var(--border);
}

.tabs button {
  border: 0;
  background: transparent;
  color: var(--text-secondary);
  padding: 16px 8px;
  font: inherit;
  cursor: pointer;
}

.tabs button[aria-selected="true"] {
  color: var(--text-primary);
  font-weight: 700;
  box-shadow: inset 0 -4px 0 rgb(var(--main-accent));
}

.composer {
  display: grid;
  grid-template-columns: 48px 1fr;
  gap: 12px;
  padding: 12px 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius-2xl);
}

.composer-placeholder {
  color: var(--text-secondary);
  margin: 0 0 16px;
}

.composer-actions {
  display: flex;
  justify-content: flex-end;
}

.token-note {
  font-size: 14px;
  color: var(--text-secondary);
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: var(--twitter-icon);
  flex-shrink: 0;
  transition: filter 200ms;
}

.avatar:hover {
  filter: brightness(0.75);
}
```

Replace `#controls` in `index.html` with:

```html
        <section id="controls">
          <h2>Controls</h2>
          <p class="token-note">Hover / focus each control. Tokens: --main-accent, --text-primary / 10, --accent-red / 10.</p>
          <div class="catalog-row">
            <button type="button" class="icon-button" data-control="icon" aria-label="Icon button">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 19l-7-7 7-7"/></svg>
            </button>
            <button type="button" class="tweet-cta" data-control="tweet-cta">Tweet</button>
            <button type="button" class="btn-follow" data-control="follow">Follow</button>
            <button type="button" class="btn-following" data-control="following">
              <span class="idle">Following</span>
              <span class="hover">Unfollow</span>
            </button>
          </div>
          <form class="search" data-control="search" action="#" onsubmit="return false">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3"/></svg>
            <input type="search" placeholder="Search Twitter" />
          </form>
          <div class="tabs" data-control="tab" role="tablist">
            <button type="button" role="tab" aria-selected="true">For you</button>
            <button type="button" role="tab" aria-selected="false">Following</button>
          </div>
          <div class="composer" data-control="composer">
            <div class="avatar" aria-hidden="true"></div>
            <div>
              <p class="composer-placeholder">What's happening?</p>
              <div class="composer-actions">
                <button type="button" class="tweet-cta" disabled>Tweet</button>
              </div>
            </div>
          </div>
        </section>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_html.HtmlChromeTest.test_controls -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_html.py site.css index.html
git commit -m "feat: add static control specimens"
```

---

### Task 7: Pattern catalog

**Files:**
- Modify: `tests/test_html.py`
- Modify: `site.css`
- Modify: `index.html` (`#patterns`)

**Interfaces:**
- Consumes: control classes from Task 6 (`.tweet-cta`, `.avatar`)
- Produces: `data-pattern` values `avatar`, `tweet`, `sidebar`, `menu`, `header`

- [ ] **Step 1: Write the failing test**

Append to `HtmlChromeTest`:

```python
    def test_patterns(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for pattern in ("avatar", "tweet", "sidebar", "menu", "header"):
            self.assertIn(f'data-pattern="{pattern}"', html)
        self.assertIn("Pinned Tweet", html)
        self.assertIn("@alice", html)
        for label in ("Home", "Explore", "Notifications", "Messages", "Bookmarks", "Lists", "Profile"):
            self.assertIn(label, html)
        self.assertIn("Delete", html)
        self.assertIn("Pin to your profile", html)
        self.assertIn("Bookmark", html)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_html.HtmlChromeTest.test_patterns -v`

Expected: FAIL (`data-pattern` missing).

- [ ] **Step 3: Write minimal implementation**

Append to `site.css`:

```css
.tweet-card {
  display: grid;
  grid-template-columns: 48px 1fr;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  transition: background-color 200ms;
}

html[data-theme="default"] .tweet-card:hover {
  background: rgb(0 0 0 / 0.03);
}

html[data-theme="lights-out"] .tweet-card:hover,
html[data-theme="dim"] .tweet-card:hover {
  background: rgb(255 255 255 / 0.03);
}

.tweet-meta {
  font-size: 14px;
  color: var(--text-secondary);
}

.tweet-name {
  font-weight: 700;
  color: var(--text-primary);
}

.tweet-body {
  margin: 4px 0 8px;
  font-size: 16px;
}

.tweet-actions {
  display: flex;
  justify-content: space-between;
  max-width: 400px;
  color: var(--text-secondary);
}

.tweet-actions button {
  border: 0;
  background: transparent;
  color: inherit;
  cursor: pointer;
  padding: 4px;
}

.tweet-actions .reply:hover,
.tweet-actions .share:hover {
  color: rgb(var(--accent-blue));
}

.tweet-actions .retweet:hover {
  color: rgb(var(--accent-green));
}

.tweet-actions .like:hover {
  color: rgb(var(--accent-pink));
}

.sidebar-demo {
  width: 260px;
  padding: 12px;
  background: rgb(var(--main-sidebar-background));
  border-radius: var(--radius-2xl);
}

.sidebar-demo a {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  border-radius: var(--radius-full);
  text-decoration: none;
  font-size: 20px;
}

.sidebar-demo a[aria-current="page"] {
  font-weight: 700;
}

.sidebar-demo .tweet-cta {
  width: 100%;
  margin-top: 12px;
}

.logo-mark {
  color: var(--twitter-icon);
  padding: 12px;
}

html[data-theme="default"] .logo-mark {
  color: rgb(var(--accent-blue));
}

.menu-demo {
  width: 260px;
  border-radius: var(--radius-md);
  background: rgb(var(--main-background));
  box-shadow: #65778633 0 0 15px, #65778626 0 0 3px 1px;
}

html[data-theme="lights-out"] .menu-demo,
html[data-theme="dim"] .menu-demo {
  box-shadow: #ffffff33 0 0 15px, #ffffff26 0 0 3px 1px;
}

.menu-demo button {
  display: block;
  width: 100%;
  text-align: left;
  border: 0;
  background: transparent;
  color: var(--text-primary);
  padding: 12px 16px;
  cursor: pointer;
}

html[data-theme="default"] .menu-demo button:hover {
  background: rgb(0 0 0 / 0.03);
}

html[data-theme="lights-out"] .menu-demo button:hover,
html[data-theme="dim"] .menu-demo button:hover {
  background: rgb(255 255 255 / 0.03);
}

.header-demo {
  padding: 8px 16px;
  background: rgb(var(--main-background) / 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
}

.header-demo h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
}
```

Replace `#patterns` in `index.html` with:

```html
        <section id="patterns">
          <h2>Patterns</h2>
          <div class="avatar" data-pattern="avatar" title="48px avatar"></div>
          <article class="tweet-card" data-pattern="tweet">
            <div class="avatar"></div>
            <div>
              <p class="type-meta">Pinned Tweet</p>
              <div class="tweet-meta">
                <span class="tweet-name">Alice</span>
                <span>@alice</span>
                <span>·</span>
                <span>2h</span>
              </div>
              <p class="tweet-body">Design tokens from the clone, not a live timeline.</p>
              <div class="tweet-actions">
                <button type="button" class="reply">Reply</button>
                <button type="button" class="retweet">Retweet</button>
                <button type="button" class="like">Like</button>
                <button type="button" class="share">Share</button>
              </div>
            </div>
          </article>
          <nav class="sidebar-demo" data-pattern="sidebar">
            <div class="logo-mark" aria-label="X">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.74l7.726-8.835L1.254 2.25H8.08l4.261 5.737 5.903-5.737zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </div>
            <a href="#patterns" aria-current="page">Home</a>
            <a href="#patterns">Explore</a>
            <a href="#patterns">Notifications</a>
            <a href="#patterns">Messages</a>
            <a href="#patterns">Bookmarks</a>
            <a href="#patterns">Lists</a>
            <a href="#patterns">Profile</a>
            <button type="button" class="tweet-cta">Tweet</button>
          </nav>
          <div class="menu-demo" data-pattern="menu">
            <button type="button">Delete</button>
            <button type="button">Pin to your profile</button>
            <button type="button">Bookmark</button>
          </div>
          <div class="header-demo" data-pattern="header">
            <h3>Home</h3>
          </div>
        </section>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_html.HtmlChromeTest.test_patterns -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_html.py site.css index.html
git commit -m "feat: add tweet, sidebar, menu, and header patterns"
```

---

### Task 8: Acceptance locks

**Files:**
- Modify: `tests/test_html.py`
- Modify: `.gitignore` only if a new ignore is required (do not add Chirp files)

**Interfaces:**
- Consumes: all previous files
- Produces: failing-closed checks for Chirp binaries, `fetch(`, and required runtime files

- [ ] **Step 1: Write the failing test**

Append to `HtmlChromeTest`:

```python
    def test_no_chirp_font_files(self):
        forbidden = list(ROOT.rglob("*.woff")) + list(ROOT.rglob("*.woff2"))
        self.assertEqual(forbidden, [])

    def test_no_network_calls_in_theme(self):
        js = (ROOT / "theme.js").read_text(encoding="utf-8")
        self.assertNotIn("fetch(", js)
        self.assertNotIn("XMLHttpRequest", js)

    def test_runtime_files_exist(self):
        for name in ("index.html", "tokens.css", "site.css", "theme.js"):
            self.assertTrue((ROOT / name).is_file(), name)
```

If `theme.js` already has no `fetch(`, this test will pass on first run after the methods exist. That is acceptable GREEN as long as Step 2 is run on a temporary edit first:

- [ ] **Step 2: Run test to verify the Chirp check can fail**

Create an empty file `tests/_tmp.woff`, then run:

`python3 -m unittest tests.test_html.HtmlChromeTest.test_no_chirp_font_files -v`

Expected: FAIL (`tests/_tmp.woff` in `forbidden`).

Delete `tests/_tmp.woff` immediately.

- [ ] **Step 3: Keep implementation as-is (no Chirp, no fetch)**

Do not add font files. Do not add network code.

- [ ] **Step 4: Run the full suite**

```bash
python3 -m unittest tests/test_tokens.py tests/test_html.py -v
node --test tests/test_theme.js
```

Expected: all PASS.

Manual check (not optional for the implementer): open `index.html`, confirm Lights out + blue, click Dim / Default and Pink, confirm Tweet CTA / tab underline / search focus ring recolor, shrink viewport below 500px and confirm `#rail` is gone while `#theme-bar` stays.

- [ ] **Step 5: Commit**

```bash
git add tests/test_html.py
git commit -m "test: lock acceptance for fonts, network, and runtime files"
```

---

## Self-review notes

Spec coverage:

| Spec item | Task |
|---|---|
| `tokens.css` RGB tables | 1 |
| Theme/accent + localStorage | 2 |
| IA, sticky bar, 500px rail | 3 |
| Overview + Chirp note | 3 |
| Color five groups + reply/image swatches | 4 |
| Type scale + underline | 5 |
| Space / radius / 200ms | 5 |
| Controls including disabled composer | 6 |
| Patterns including menu rows and Home header | 7 |
| Acceptance 1–7 | 8 + manual open |

No TBD. Function names stay `applyTheme`, `applyAccent`, `persist`, `loadPersisted`, `boot` across Task 2 and Task 3.
