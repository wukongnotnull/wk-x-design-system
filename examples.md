# Showcase examples

Showcase catalog distilled from https://github.com/ccrsxx/twitter-clone (`62a9588`) plus a logged-in x.com extract captured 2026-09-16. Do not re-clone that repo or re-fetch x.com for tokens.

**Root:** `showcase/` next to `SKILL.md` (resolve from the directory containing this file)

**Open:** `showcase/index.html` (or `python3 -m http.server` from `showcase/`)

**Source:** `clone` = ccrsxx/twitter-clone at `62a9588`; `x.com 2026-09` = x.com extract, 2026-09-16. Use `x.com 2026-09` rows only when the user asks for current-X chrome; do not mix the two eras inside one component.

For each task: grep `showcase/site.css` for the selector column. Markup is in `showcase/index.html` at the `data-*` hook.

### Foundations

| Task | Source | Markup hook | Grep in `site.css` |
|---|---|---|---|
| Theme / accent chrome | `clone` | `[data-set-theme]`, `[data-set-accent]` | `#theme-bar`, `.picker` |
| Color tokens | `clone` | `[data-color-group]`, `[data-token]` | `.swatch` |
| Type scale | `clone` | `[data-type]` | `.type-display`, `.type-title`, `.type-body`, `.type-meta`, `.type-secondary`, `.custom-underline` |
| Space / radius | `clone` | `.space-box`, `.radius-demo` | `.radius-demo` |

### Controls

| Task | Source | Markup hook | Grep in `site.css` |
|---|---|---|---|
| Icon button | `clone` | `[data-control="icon"]` | `.icon-button` |
| Tweet CTA | `clone` | `[data-control="tweet-cta"]` | `.tweet-cta` |
| Follow | `clone` | `[data-control="follow"]` | `.btn-follow` |
| Following → Unfollow | `clone` | `[data-control="following"]` | `.btn-following` |
| Search | `clone` | `[data-control="search"]` | `.search` |
| For you / Following tabs | `clone` | `[data-control="tab"]` | `.tabs` |
| Composer | `clone` | `[data-control="composer"]` | `.composer`, `.composer-option`, `.avatar` |

### Icons

| Task | Source | Markup hook | Grep in `site.css` |
|---|---|---|---|
| Icons | `clone` + `x.com 2026-09` — per-icon `source` in `showcase/icons/manifest.json` | `[data-icon]`, `showcase/icons/` | `.icon-grid`, `.icon-swatch` |

### Patterns — clone `62a9588`

| Task | Source | Markup hook | Grep in `site.css` |
|---|---|---|---|
| Avatar | `clone` | `[data-pattern="avatar"]` | `.avatar` |
| Home shell | `clone` | `[data-pattern="home"]` | `.home-shell`, `.home-main` |
| Tweet row | `clone` | `[data-pattern="tweet"]` | `.tweet-card`, `.hover-card`, `.accent-tab`, `.tweet-status`, `.tweet-verified`, `.tweet-more`, `.tweet-rail`, `.reply-line`, `.media-grid`, `.tweet-actions`, `.disc`, `.tweet-count`, `.like.is-liked`, `.retweet.is-retweeted` |
| Sidebar | `clone` | `[data-pattern="sidebar"]`, `[data-nav-icon]` | `.sidebar-demo`, `.logo-mark` |
| Overflow menu | `clone` | `[data-pattern="menu"]` | `.menu-demo` |
| Blur header | `clone` | `[data-pattern="header"]` | `.header-demo` |
| Trends | `clone` | `[data-pattern="trends"]` | `.aside-card`, `.trend-row`, `.aside-more` |
| Who to follow | `clone` | `[data-pattern="who-to-follow"]` | `.aside-card`, `.suggest-row`, `.btn-follow` |
| Profile cover | `clone` | `[data-pattern="profile"]` | `.profile-cover`, `.profile-home-avatar` |
| Profile UserNav | `clone` | `[data-pattern="profile"]` | `.user-nav`, `.user-nav-link`, `.user-nav-underline` |
| Profile UserDetails | `clone` | `[data-pattern="profile"]` | `.user-details`, `.user-detail`, `.user-follow-stats`, `.user-website` |
| Image lightbox | `clone` | `[data-pattern="image-modal"]` | `.image-modal`, `.image-modal-backdrop`, `.image-modal-arrow`, `.image-modal-img` |
| Tooltip | `clone` | `[data-pattern="tooltip"]` | `.tooltip-host`, `.tooltip` |
| Aside footer | `clone` | `[data-pattern="aside-footer"]` | `.aside-footer` |
| Float label | `clone` | `[data-pattern="float-label"]` | `.float-label-field`, `.float-label-count` |
| Home composer | `clone` | `[data-pattern="home"]` `.home-main .composer` | `.home-main .composer` |
| Aside search | `clone` | `[data-pattern="aside-search"]` | `.aside-search`, `.search-clear` |
| Media grid 1 / 2 / 3 / 4 | `clone` | `[data-pattern="media-grid"]` | `.media-grid[data-count="1"]`, `.media-grid[data-count="2"]`, `.media-grid[data-count="3"]`, `.media-grid[data-count="4"]` |
| Empty cover fallback | `clone` | `[data-pattern="profile-empty"]` | `.profile-cover.is-empty` |
| Action confirm modal | `clone` | `[data-pattern="action-modal"]` | `.action-modal`, `.action-modal-panel`, `.action-modal-main` |
| Loading | `clone` | `[data-pattern="loading"]` | `.status-loading` |
| Error | `clone` | `[data-pattern="error"]` | `.status-error` |
| Composer progress bar | `clone` | `[data-pattern="progress-bar"]` | `.progress-bar`, `.progress-bar[data-state="ok"]`, `.progress-bar[data-state="warn"]`, `.progress-bar[data-state="over"]` |
| Stats empty | `clone` | `[data-pattern="stats-empty"]` | `.stats-empty` |
| User hover-card | `clone` | `[data-pattern="user-hover"]` | `.user-hover-host`, `.user-hover-card`, `.user-hover-cover.is-empty`, `.user-follows-you` |
| Edit profile modal | `clone` | `[data-pattern="edit-profile"]` | `.edit-profile`, `.edit-profile-cover`, `.edit-profile-camera` |
| Username modal | `clone` | `[data-pattern="username-modal"]` | `.username-modal`, `.username-modal-main`, `.username-modal-skip` |
| Mobile sidebar | `clone` | `[data-pattern="mobile-sidebar"]` | `.mobile-sidebar`, `.mobile-sidebar-panel` |
| Reply modal | `clone` | `[data-pattern="reply-modal"]` | `.reply-modal`, `.reply-modal-panel` |
| Stats modal | `clone` | `[data-pattern="stats-modal"]` | `.stats-modal`, `.stats-modal-header` |
| Clone auth landing | `clone` | `[data-pattern="auth-landing-clone"]` | `.auth-landing-clone`, `.auth-clone-banner` |
| Sidebar logout popover | `clone` | `[data-pattern="logout-popover"]` | `.logout-popover`, `.logout-caret` |
| Clone More menu | `clone` | `[data-pattern="clone-more"]` | `.clone-more-demo` |
| Tweet share popover | `clone` | `[data-pattern="tweet-share"]` | `.tweet-share-demo` |
| Tweet overflow with icons | `clone` | `[data-pattern="tweet-overflow"]` | `.tweet-overflow-demo`, `.is-danger` |
| Profile More + Message | `clone` | `[data-pattern="profile-actions"]` | `.profile-actions`, `.icon-only` |
| People user-card | `clone` | `[data-pattern="user-card"]` | `.user-card`, `.user-card-top` |
| Composer preview 4-up | `clone` | `[data-pattern="composer-preview"]` | `.composer-preview-demo`, `.media-remove` |
| Status count text | `clone` | `[data-pattern="status-counts"]` | `.status-counts` |
| Missing account | `clone` | `[data-pattern="account-missing"]` | `.account-missing` |

### Patterns — x.com extract 2026-09-16

| Task | Source | Markup hook | Grep in `site.css` |
|---|---|---|---|
| Auth landing | `x.com 2026-09` | `[data-pattern="auth-landing"]` | `.auth-landing`, `.btn-social`, `.auth-field`, `.btn-continue`, `.auth-or` |
| Login modal | `x.com 2026-09` | `[data-pattern="login-modal"]` | `.login-modal`, `.login-modal-panel`, `.login-modal-backdrop` |
| Signup aside | `x.com 2026-09` | `[data-pattern="signup-aside"]` | `.signup-aside`, `.btn-social` |
| Profile Mention + Follow | `x.com 2026-09` | `[data-pattern="profile-mention"]` | `.btn-outline`, `.profile-mention-demo` |
| Page header | `x.com 2026-09` | `[data-pattern="page-header"]` | `.page-header`, `.tweet-verified.is-gold` |
| Quote embed | `x.com 2026-09` | `[data-pattern="quote-embed"]` | `.quote-embed` |
| Video media | `x.com 2026-09` | `[data-pattern="video-media"]` | `.video-media`, `.video-play`, `.video-duration` |
| Views + bookmark | `x.com 2026-09` | `[data-pattern="tweet-metrics"]` | `.tweet-actions.is-wide`, `.tweet-actions .views`, `.tweet-actions .bookmark` |
| Post detail | `x.com 2026-09` | `[data-pattern="post-detail"]` | `.status-detail`, `.tweet-card.is-status`, `.status-time` |
| Account switcher | `x.com 2026-09` | `[data-pattern="account-switcher"]` | `.account-switcher`, `.account-switcher-meta` |
| Topic tabs | `x.com 2026-09` | `[data-pattern="topic-tabs"]` | `.tabs.is-scroll`, `.topic-add` |
| Today's News | `x.com 2026-09` | `[data-pattern="news-aside"]` | `.news-row`, `.news-headline` |
| Explore | `x.com 2026-09` | `[data-pattern="explore"]` | `.explore-demo`, `.tabs.is-five` |
| Notifications | `x.com 2026-09` | `[data-pattern="notifications"]` | `.notifications-demo`, `.notice-row`, `.notice-mark` |
| Search results | `x.com 2026-09` | `[data-pattern="search-results"]` | `.search-results-demo` |
| Search filters | `x.com 2026-09` | `[data-pattern="search-filters"]` | `.filter-row`, `.filter-legend`, `.filter-row.is-on` |
| Direct Messages | `x.com 2026-09` | `[data-pattern="messages"]` | `.messages-demo`, `.messages-list`, `.messages-pane`, `.messages-row` |
| Poll composer | `x.com 2026-09` | `[data-pattern="poll"]` | `.poll-modal`, `.poll-choice`, `.poll-length`, `.poll-remove` |
| See new posts | `x.com 2026-09` | `[data-pattern="new-posts"]` | `.new-posts` |
| Search relevant | `x.com 2026-09` | `[data-pattern="search-relevant"]` | `.search-relevant`, `.search-relevant-actions` |
| Communities page | `x.com 2026-09` | `[data-pattern="communities"]` | `.communities-demo`, `.community-card`, `.community-chip` |
| More-menu destinations | `x.com 2026-09` | `[data-pattern="more-menu"]` | `.more-menu-demo` |
| Display modal | `x.com 2026-09` | `[data-pattern="display-modal"]` | `.display-modal`, `.accent-radio`, `.theme-radio` |
| Grok page chrome | `x.com 2026-09` | `[data-pattern="grok"]` | `.grok-demo`, `.grok-prompt`, `.voice-bars` |
| Premium page chrome | `x.com 2026-09` | `[data-pattern="premium"]` | `.premium-demo`, `.premium-card`, `.premium-upgrade` |
| Articles editor chrome | `x.com 2026-09` | `[data-pattern="articles"]` | `.articles-demo`, `.article-draft`, `.articles-empty` |

### Responsive

| Task | Source | Markup hook | Grep in `site.css` |
|---|---|---|---|
| Hide catalog rail < 500px | `clone` | `#rail` | `@media (max-width: 499px)` |
| Responsive: icon-only sidebar < 1280 (xl) | `clone` | `[data-pattern="sidebar"]`, `.nav-label`, `.nav-feather` | `@media (max-width: 1279px)`, `.sidebar-demo .nav-label`, `.sidebar-demo .nav-feather` |
| Responsive: sidebar 96px at 768–1279 (md) | `clone` | `[data-pattern="sidebar"]` | `@media (min-width: 768px) and (max-width: 1279px)` |
| Responsive: aside removed < 1024 (lg) | `clone` | `.aside-stack` | `@media (max-width: 1023px)` |
| Responsive: bottom tab bar < 500 (xs) | `clone` | `[data-pattern="sidebar"]`, `[data-can-hide]` | `@media (max-width: 499px)`, `.sidebar-demo a[data-can-hide]`, `.sidebar-demo .tweet-cta` |

Breakpoints come from the clone's `tailwind.config.js` at `62a9588`: `xs 500px`, then Tailwind defaults `sm 640 / md 768 / lg 1024 / xl 1280`. Sidebar labels show at `xl` only; `data-can-hide` marks the clone's `canBeHidden` links (Explore, Bookmarks, Lists), which drop from the mobile bar.

`theme.js` only shows how to persist `xds-theme` / `xds-accent`. Do not copy it unless the user asked for a theme switcher. The `#theme-bar` picker is catalog chrome — leave the product accent blue.
