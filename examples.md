# Showcase examples

Live catalog distilled from https://github.com/ccrsxx/twitter-clone (`62a9588`). Do not re-clone that repo for tokens.

**Root:** `showcase/` next to `SKILL.md` (`/Users/wukong/.agents/skills/wk-x-design-system/showcase`)

**Open:** `showcase/index.html` (or `python3 -m http.server` from `showcase/`)

For each task: grep `showcase/site.css` for the selector column. Markup is in `showcase/index.html` at the section / `data-*` hook.

| Task | Section | Markup hook | Grep in `site.css` |
|---|---|---|---|
| Theme / accent chrome | `#theme-bar` | `[data-set-theme]`, `[data-set-accent]` | `#theme-bar`, `.picker` |
| Color tokens | `#color` | `[data-color-group]`, `[data-token]` | `.swatch` |
| Type scale | `#type` | `[data-type]` | `.type-display`, `.type-title`, `.type-body`, `.type-meta`, `.type-secondary`, `.custom-underline` |
| Space / radius | `#space` | `.space-box`, `.radius-demo` | `.radius-demo` |
| Icon button | `#controls` | `[data-control="icon"]` | `.icon-button` |
| Tweet CTA | `#controls` | `[data-control="tweet-cta"]` | `.tweet-cta` |
| Follow | `#controls` | `[data-control="follow"]` | `.btn-follow` |
| Following → Unfollow | `#controls` | `[data-control="following"]` | `.btn-following` |
| Search | `#controls` | `[data-control="search"]` | `.search` |
| For you / Following tabs | `#controls` | `[data-control="tab"]` | `.tabs` |
| Composer | `#controls` | `[data-control="composer"]` | `.composer`, `.composer-option`, `.avatar` |
| Avatar | `#patterns` | `[data-pattern="avatar"]` | `.avatar` |
| Icons | `#icons` | `[data-icon]`, `showcase/icons/` | `.icon-grid`, `.icon-swatch` |
| Home shell | `#patterns` | `[data-pattern="home"]` | `.home-shell`, `.home-main` |
| Tweet row | `#patterns` | `[data-pattern="tweet"]` | `.tweet-card`, `.hover-card`, `.accent-tab`, `.tweet-status`, `.tweet-verified`, `.tweet-more`, `.tweet-rail`, `.reply-line`, `.media-grid`, `.tweet-actions`, `.disc`, `.tweet-count`, `.like.is-liked`, `.retweet.is-retweeted` |
| Sidebar | `#patterns` | `[data-pattern="sidebar"]` | `.sidebar-demo`, `[data-nav-icon]`, `.logo-mark` |
| Overflow menu | `#patterns` | `[data-pattern="menu"]` | `.menu-demo` |
| Blur header | `#patterns` | `[data-pattern="header"]` | `.header-demo` |
| Trends | `#patterns` | `[data-pattern="trends"]` | `.aside-card`, `.trend-row`, `.aside-more` |
| Who to follow | `#patterns` | `[data-pattern="who-to-follow"]` | `.aside-card`, `.suggest-row`, `.btn-follow` |
| Profile cover | `#patterns` | `[data-pattern="profile"]` | `.profile-cover`, `.profile-home-avatar` |
| Profile UserNav | `#patterns` | `[data-pattern="profile"]` | `.user-nav`, `.user-nav-link`, `.user-nav-underline` |
| Profile UserDetails | `#patterns` | `[data-pattern="profile"]` | `.user-details`, `.user-detail`, `.user-follow-stats`, `.user-website` |
| Image lightbox | `#patterns` | `[data-pattern="image-modal"]` | `.image-modal`, `.image-modal-backdrop`, `.image-modal-arrow`, `.image-modal-img` |
| Tooltip | `#patterns` | `[data-pattern="tooltip"]` | `.tooltip-host`, `.tooltip` |
| Aside footer | `#patterns` | `[data-pattern="aside-footer"]` | `.aside-footer` |
| Float label | `#patterns` | `[data-pattern="float-label"]` | `.float-label-field`, `.float-label-count` |
| Home composer | `#patterns` | `[data-pattern="home"]` `.home-main .composer` | `.home-main .composer` |
| Aside search | `#patterns` | `[data-pattern="aside-search"]` | `.aside-search`, `.search-clear` |
| Media grid 1 / 2 / 3 | `#patterns` | `[data-pattern="media-grid"]` | `.media-grid[data-count="1"]`, `.media-grid[data-count="2"]`, `.media-grid[data-count="3"]` |
| Empty cover fallback | `#patterns` | `[data-pattern="profile-empty"]` | `.profile-cover.is-empty` |
| Action confirm modal | `#patterns` | `[data-pattern="action-modal"]` | `.action-modal`, `.action-modal-panel`, `.action-modal-main` |
| Loading | `#patterns` | `[data-pattern="loading"]` | `.status-loading` |
| Error | `#patterns` | `[data-pattern="error"]` | `.status-error` |
| Composer progress bar | `#patterns` | `[data-pattern="progress-bar"]` | `.progress-bar`, `.progress-bar[data-state="ok"]`, `.progress-bar[data-state="warn"]`, `.progress-bar[data-state="over"]` |
| Stats empty | `#patterns` | `[data-pattern="stats-empty"]` | `.stats-empty` |
| User hover-card | `#patterns` | `[data-pattern="user-hover"]` | `.user-hover-host`, `.user-hover-card`, `.user-hover-cover.is-empty`, `.user-follows-you` |
| Edit profile modal | `#patterns` | `[data-pattern="edit-profile"]` | `.edit-profile`, `.edit-profile-cover`, `.edit-profile-camera` |
| Username modal | `#patterns` | `[data-pattern="username-modal"]` | `.username-modal`, `.username-modal-main`, `.username-modal-skip` |
| Mobile sidebar | `#patterns` | `[data-pattern="mobile-sidebar"]` | `.mobile-sidebar`, `.mobile-sidebar-panel` |
| Reply modal | `#patterns` | `[data-pattern="reply-modal"]` | `.reply-modal`, `.reply-modal-panel` |
| Stats modal | `#patterns` | `[data-pattern="stats-modal"]` | `.stats-modal`, `.stats-modal-header` |
| Hide left rail < 500px | layout | `#rail` | `@media (max-width: 499px)` |

`theme.js` only shows how to persist `xds-theme` / `xds-accent`. Do not copy it unless the user asked for a theme switcher. The `#theme-bar` picker is catalog chrome — leave the product accent blue.
