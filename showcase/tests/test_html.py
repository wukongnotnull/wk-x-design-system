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
        for section_id in ("overview", "color", "type", "space", "controls", "icons", "patterns"):
            self.assertIn(f'id="{section_id}"', HTML)

    def test_theme_and_accent_buttons(self):
        for theme in ("lights-out", "dim", "default"):
            self.assertIn(f'data-set-theme="{theme}"', HTML)
        for accent in ("blue", "yellow", "pink", "purple", "orange", "green"):
            self.assertIn(f'data-set-accent="{accent}"', HTML)

    def test_rail_hidden_below_500px(self):
        self.assertIn("@media (max-width: 499px)", SITE)
        self.assertIn("#rail", SITE)

    def test_section_scroll_margin_clears_sticky_bar(self):
        self.assertIn("scroll-margin-top: 72px", SITE)

    def test_overview_mentions_chirp_fallback(self):
        self.assertIn("Chirp", HTML)
        self.assertIn("system-ui", HTML)

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

    def test_controls(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for control in ("icon", "tweet-cta", "follow", "following", "search", "tab", "composer"):
            self.assertIn(f'data-control="{control}"', html)
        self.assertIn("What's happening?", html)
        self.assertIn("disabled", html)
        self.assertIn("For you", html)
        self.assertIn("Following", html)

    def test_patterns(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for pattern in (
            "avatar",
            "tweet",
            "sidebar",
            "menu",
            "header",
            "trends",
            "who-to-follow",
            "home",
            "profile",
            "image-modal",
            "tooltip",
            "aside-footer",
            "float-label",
            "aside-search",
            "media-grid",
            "profile-empty",
            "action-modal",
            "loading",
            "error",
            "progress-bar",
            "stats-empty",
            "user-hover",
            "edit-profile",
            "username-modal",
            "mobile-sidebar",
            "reply-modal",
            "stats-modal",
            "auth-landing",
            "login-modal",
            "signup-aside",
            "profile-mention",
            "page-header",
            "quote-embed",
            "video-media",
            "tweet-metrics",
            "post-detail",
            "account-switcher",
            "topic-tabs",
            "news-aside",
            "explore",
            "notifications",
            "search-results",
            "search-filters",
            "messages",
            "poll",
            "new-posts",
            "search-relevant",
            "communities",
            "more-menu",
            "display-modal",
            "auth-landing-clone",
            "logout-popover",
            "clone-more",
            "tweet-share",
            "tweet-overflow",
            "profile-actions",
            "user-card",
            "composer-preview",
            "status-counts",
            "account-missing",
        ):
            self.assertIn(f'data-pattern="{pattern}"', html)
        self.assertIn("Pinned Tweet", html)
        self.assertIn("@alice", html)
        for label in ("Home", "Explore", "Notifications", "Messages", "Bookmarks", "Lists", "Profile"):
            self.assertIn(label, html)
        self.assertIn("Delete", html)
        self.assertIn("Pin to your profile", html)
        self.assertIn("Bookmark", html)

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

    def test_tweet_action_hover_disc(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn('class="disc"', html)
        self.assertIn(".tweet-actions .disc", css)
        self.assertIn("rgb(var(--accent-blue) / 0.1)", css)
        self.assertIn("rgb(var(--accent-green) / 0.1)", css)
        self.assertIn("rgb(var(--accent-pink) / 0.1)", css)
        self.assertIn("rgb(var(--accent-blue) / 0.2)", css)

    def test_sidebar_nav_icons_28px(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        for name in (
            "HomeIcon",
            "HashtagIcon",
            "BellIcon",
            "EnvelopeIcon",
            "BookmarkIcon",
            "Bars3BottomLeftIcon",
            "UserIcon",
        ):
            self.assertIn(f'data-nav-icon="{name}"', html)
        self.assertIn(".sidebar-demo svg", css)
        self.assertIn("width: 28px", css)

    def test_composer_option_row(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn("composer-options", html)
        self.assertIn('aria-label="Media"', html)
        self.assertIn('aria-label="GIF"', html)
        self.assertIn('aria-label="Poll"', html)
        self.assertIn('aria-label="Emoji"', html)
        self.assertIn('aria-label="Schedule"', html)
        self.assertIn('aria-label="Location"', html)
        self.assertIn(".composer-option", css)
        self.assertIn("rgb(var(--main-accent) / 0.1)", css)

    def test_tweet_action_counts(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn('class="tweet-count"', html)
        self.assertIn(".tweet-actions .tweet-count", css)
        self.assertIn("14px", css)
        self.assertGreaterEqual(html.count('class="tweet-count"'), 3)

    def test_liked_heart_fill(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn("is-liked", html)
        self.assertIn('aria-pressed="true"', html)
        self.assertIn(".tweet-actions .like.is-liked svg", css)
        self.assertIn("fill: rgb(var(--accent-pink))", css)

    def test_retweeted_stroke(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn("is-retweeted", html)
        self.assertIn('aria-label="Undo Retweet"', html)
        self.assertIn(".tweet-actions .retweet.is-retweeted", css)
        self.assertIn(".tweet-actions .retweet.is-retweeted svg", css)
        self.assertIn("stroke-width: 2px", css)
        self.assertIn("color: rgb(var(--accent-green))", css)

    def test_tweet_header_pin_verified_more(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        tweet = html[html.index('data-pattern="tweet"') : html.index('data-pattern="trends"')]
        self.assertIn('class="tweet-status"', tweet)
        self.assertIn('data-icon="PinIcon"', tweet)
        self.assertIn('data-icon="CheckBadgeIcon"', tweet)
        self.assertIn('class="tweet-verified"', tweet)
        self.assertIn('aria-label="More"', tweet)
        self.assertIn('data-icon="EllipsisHorizontalIcon"', tweet)
        self.assertIn(".tweet-status", css)
        self.assertIn("rotate(-45deg)", css)
        self.assertIn(".tweet-verified", css)
        self.assertIn("fill: rgb(var(--accent-blue))", css)
        self.assertIn(".tweet-more", css)

    def test_tweet_reply_line(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        tweet = html[html.index('data-pattern="tweet"') : html.index('data-pattern="trends"')]
        self.assertIn('class="tweet-rail"', tweet)
        self.assertIn('class="reply-line"', tweet)
        self.assertIn("Replying to", tweet)
        self.assertIn(".tweet-rail", css)
        self.assertIn(".reply-line", css)
        self.assertIn("background: var(--reply-line)", css)
        self.assertIn("width: 2px", css)

    def test_tweet_hover_card_accent_tab(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        tweet = html[html.index('data-pattern="tweet"') : html.index('data-pattern="trends"')]
        self.assertIn("hover-card", tweet)
        self.assertIn("accent-tab", tweet)
        self.assertIn(".hover-card:hover", css)
        self.assertIn(".hover-card:focus-visible", css)
        self.assertIn(".accent-tab:focus-visible", css)
        self.assertIn("box-shadow: 0 0 0 2px rgb(var(--main-accent) / 0.8)", css)

    def test_aside_trends_and_who_to_follow(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn('data-pattern="trends"', html)
        self.assertIn('data-pattern="who-to-follow"', html)
        self.assertIn("Trends for you", html)
        self.assertIn("Who to follow", html)
        self.assertIn("Trending Worldwide", html)
        self.assertIn("Show more", html)
        self.assertIn(".aside-card", css)
        self.assertIn(".trend-row", css)
        self.assertIn(".suggest-row", css)
        self.assertIn(".aside-more", css)
        self.assertIn("width: 384px", css)

    def test_home_shell_three_columns(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn('data-pattern="home"', html)
        self.assertIn("home-shell", html)
        self.assertIn("home-main", html)
        home = html[html.index('data-pattern="home"') : html.index('data-pattern="menu"')]
        self.assertLess(home.index('data-pattern="sidebar"'), home.index('data-pattern="tweet"'))
        self.assertLess(home.index('data-pattern="tweet"'), home.index('data-pattern="trends"'))
        self.assertIn('data-pattern="who-to-follow"', home)
        self.assertIn('data-pattern="header"', home)
        self.assertIn(".home-shell", css)
        self.assertIn(".home-main", css)
        self.assertIn("260px minmax(0, 576px) 384px", css)
        self.assertIn("max-width: 576px", css)

    def test_tweet_media_grid(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        tweet = html[html.index('data-pattern="tweet"') : html.index('data-pattern="trends"')]
        self.assertIn('class="media-grid"', tweet)
        self.assertIn('data-count="4"', tweet)
        self.assertGreaterEqual(tweet.count("media-cell"), 4)
        self.assertIn(".media-grid", css)
        self.assertIn("grid-template-columns: 1fr 1fr", css)
        self.assertIn("height: 271px", css)
        self.assertIn("gap: 2px", css)
        self.assertIn("brightness(0.75)", css)

    def test_profile_cover(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn('data-pattern="profile"', html)
        self.assertIn("profile-cover", html)
        self.assertIn("profile-home-avatar", html)
        self.assertIn(".profile-cover", css)
        self.assertIn(".profile-cover:hover", css)
        self.assertIn("height: 208px", css)
        self.assertIn("width: 144px", css)
        self.assertIn("translateY(-50%)", css)

    def test_image_modal_pattern(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="image-modal"', patterns)
        modal = html[html.index('data-pattern="image-modal"') :]
        self.assertIn('class="image-modal"', modal)
        self.assertIn("image-modal-backdrop", modal)
        self.assertIn('role="dialog"', modal)
        self.assertIn("Open original", modal)
        self.assertIn("custom-underline", modal)
        self.assertIn('aria-label="Previous"', modal)
        self.assertIn('aria-label="Next"', modal)
        self.assertIn('data-icon="ArrowLeftIcon"', modal)
        self.assertIn('data-icon="ArrowRightIcon"', modal)
        self.assertIn("M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18", modal)
        self.assertIn("M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3", modal)
        tweet = html[html.index('data-pattern="tweet"') : html.index('data-pattern="trends"')]
        self.assertIn('class="media-grid"', tweet)
        self.assertGreaterEqual(tweet.count("media-cell"), 4)
        self.assertIn(".image-modal", css)
        self.assertIn(".image-modal-backdrop", css)
        self.assertIn(".image-modal-arrow", css)
        self.assertIn("z-index: 50", css)
        self.assertIn("rgb(0 0 0 / 0.4)", css)
        self.assertIn("#5B7083", css)
        self.assertIn("max-height: 75vh", css)
        self.assertIn("object-fit: contain", css)

    def test_tooltip_pattern(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="tooltip"', patterns)
        tip = html[html.index('data-pattern="tooltip"') :]
        self.assertIn('class="tooltip"', tip)
        self.assertIn("tooltip-host", tip)
        self.assertIn('aria-label="More"', tip)
        self.assertIn('data-icon="EllipsisHorizontalIcon"', tip)
        self.assertIn(
            "M6.75 12a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM12.75 12a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM18.75 12a.75.75 0 11-1.5 0 .75.75 0 011.5 0z",
            tip,
        )
        self.assertIn(".tooltip-host", css)
        self.assertIn(".tooltip", css)
        self.assertIn(".tooltip-host:hover .tooltip", css)
        self.assertIn(".tooltip-host:focus-visible .tooltip", css)
        self.assertIn("#666666", css)
        self.assertIn("#495A69", css)
        self.assertIn("visibility: hidden", css)
        self.assertIn("delay: 500ms", css)

    def test_aside_footer(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="aside-footer"', patterns)
        footer = html[html.index('data-pattern="aside-footer"') :]
        home = html[html.index('data-pattern="home"') : html.index('data-pattern="menu"')]
        self.assertNotIn('data-pattern="aside-footer"', home)
        self.assertIn('class="aside-footer"', footer)
        for label in (
            "Terms of Service",
            "Privacy Policy",
            "Cookie Policy",
            "Accessibility",
            "Ads Info",
        ):
            self.assertIn(label, footer)
        self.assertIn("© 2022 Twitter, Inc.", footer)
        self.assertIn("custom-underline", footer)
        self.assertIn('target="_blank"', footer)
        self.assertIn('rel="noreferrer"', footer)
        self.assertIn("https://twitter.com/tos", footer)
        self.assertIn("https://twitter.com/privacy", footer)
        self.assertIn("https://support.twitter.com/articles/20170514", footer)
        self.assertIn("https://help.twitter.com/resources/accessibility", footer)
        self.assertIn(
            "https://business.twitter.com/en/help/troubleshooting/how-twitter-ads-work.html",
            footer,
        )
        self.assertIn(".aside-footer", css)
        self.assertIn(".aside-footer nav", css)
        self.assertIn("gap: 12px", css)
        self.assertIn("justify-content: center", css)
        self.assertIn("flex-wrap: wrap", css)

    def test_float_label(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="float-label"', patterns)
        field = html[html.index('data-pattern="float-label"') :]
        self.assertIn("float-label-field", field)
        self.assertIn("float-label-count", field)
        self.assertIn("Name can't be blank", field)
        self.assertIn("is-error", field)
        self.assertIn('placeholder="name"', field)
        self.assertIn(".float-label-field", css)
        self.assertIn(".float-label-field:focus-within", css)
        self.assertIn(":placeholder-shown ~ label", css)
        self.assertIn(".float-label-field input:focus ~ label", css)
        self.assertIn("translateY(12px)", css)
        self.assertIn("translateY(4px)", css)
        self.assertIn("margin-top: 24px", css)
        self.assertIn(".float-label-field.is-error", css)
        self.assertIn(".float-label-count", css)
        label_css = css[
            css.index(".float-label-field label") : css.index(
                ".float-label-field input:placeholder-shown"
            )
        ]
        self.assertIn("top: 0", label_css)

    def test_profile_user_nav(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        profile = html[html.index('data-pattern="profile"') :]
        self.assertIn('class="user-nav"', profile)
        self.assertLess(profile.index("profile-cover"), profile.index("user-nav"))
        self.assertIn("user-nav-link", profile)
        self.assertIn("user-nav-underline", profile)
        for label in ("Tweets", "Replies", "Media", "Likes"):
            self.assertIn(label, profile)
        tweets_block = profile[profile.index("Tweets") - 160 : profile.index("Media")]
        self.assertIn('aria-selected="true"', tweets_block)
        self.assertIn(".user-nav", css)
        self.assertIn(".user-nav-link", css)
        self.assertIn(".user-nav-underline", css)
        self.assertIn('.user-nav-link[aria-selected="true"]', css)
        self.assertIn("transform: scale(0.5)", css)
        self.assertIn("transform: scale(1)", css)

    def test_profile_user_details(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        start = html.index('data-pattern="profile"')
        nxt = html.find('data-pattern="', start + 1)
        profile = html[start: nxt if nxt != -1 else None]
        self.assertIn("user-details", profile)
        self.assertLess(profile.index("@alice"), profile.index("user-details"))
        self.assertLess(profile.index("user-details"), profile.index("user-nav"))
        self.assertIn("user-bio", profile)
        self.assertIn("user-follow-stats", profile)
        self.assertIn("Following", profile)
        self.assertIn("Followers", profile)
        self.assertIn("Joined", profile)
        self.assertIn('data-icon="MapPinIcon"', profile)
        self.assertIn('data-icon="LinkIcon"', profile)
        self.assertIn('data-icon="CalendarDaysIcon"', profile)
        self.assertIn("M15 10.5a3 3 0 11-6 0 3 3 0 016 0z", profile)
        self.assertIn(
            "M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244",
            profile,
        )
        self.assertIn("M6.75 3v2.25M17.25 3v2.25", profile)
        self.assertIn("custom-underline", profile)
        self.assertIn("user-website", profile)
        self.assertIn(".user-details", css)
        self.assertIn(".user-follow-stats", css)
        self.assertIn(".user-website", css)
        self.assertIn(".user-detail", css)
        self.assertIn("gap: 16px", css)

    def test_home_composer(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        home_main = html[html.index('class="home-main"') : html.index('data-pattern="tweet"')]
        self.assertIn('class="composer"', home_main)
        self.assertIn("What's happening?", home_main)
        self.assertLess(home_main.index('data-pattern="header"'), home_main.index('class="composer"'))
        self.assertIn("composer-options", home_main)
        self.assertIn('aria-label="Media"', home_main)
        self.assertIn(".home-main .composer", css)

    def test_aside_search(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        home = html[html.index('data-pattern="home"') : html.index('data-pattern="menu"')]
        self.assertIn('data-pattern="aside-search"', home)
        self.assertLess(home.index('data-pattern="aside-search"'), home.index('data-pattern="trends"'))
        search = html[html.index('data-pattern="aside-search"') : html.index('data-pattern="trends"')]
        self.assertIn('class="search', search)
        self.assertIn("Search Twitter", search)
        self.assertIn('data-icon="MagnifyingGlassIcon"', search)
        self.assertIn("M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z", search)
        self.assertIn('data-icon="XMarkIcon"', search)
        self.assertIn("M6 18L18 6M6 6l12 12", search)
        self.assertIn(".aside-search", css)
        self.assertIn("position: sticky", css)

    def test_media_grid_variants(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="media-grid"', patterns)
        grids = html[html.index('data-pattern="media-grid"') :]
        for count in ("1", "2", "3"):
            self.assertIn(f'data-count="{count}"', grids)
        self.assertIn('.media-grid[data-count="1"]', css)
        self.assertIn('.media-grid[data-count="2"]', css)
        self.assertIn('.media-grid[data-count="3"]', css)
        self.assertIn("grid-row: 1 / -1", css)

    def test_empty_cover_fallback(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="profile-empty"', patterns)
        empty = html[html.index('data-pattern="profile-empty"') :]
        self.assertIn("profile-cover", empty)
        self.assertIn("is-empty", empty)
        self.assertIn(".profile-cover.is-empty", css)
        self.assertIn("background: var(--reply-line)", css)

    def test_action_modal(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="action-modal"', patterns)
        modal = html[html.index('data-pattern="action-modal"') :]
        self.assertIn('class="action-modal"', modal)
        self.assertIn("action-modal-backdrop", modal)
        self.assertIn("action-modal-panel", modal)
        self.assertIn('role="dialog"', modal)
        self.assertIn("Delete Tweet?", modal)
        self.assertIn("This can’t be undone", modal)
        self.assertIn("Delete", modal)
        self.assertIn("Cancel", modal)
        self.assertIn(".action-modal", css)
        self.assertIn(".action-modal-panel", css)
        self.assertIn(".action-modal-main", css)
        self.assertIn("max-width: 20rem", css)
        self.assertIn("rgb(var(--accent-red))", css)

    def test_loading_and_error(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="loading"', patterns)
        self.assertIn('data-pattern="error"', patterns)
        loading = html[html.index('data-pattern="loading"') : html.index('data-pattern="error"')]
        self.assertIn('data-icon="SpinnerIcon"', loading)
        self.assertIn(
            "M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z",
            loading,
        )
        error = html[html.index('data-pattern="error"') :]
        self.assertIn("Something went wrong. Try Loading.", error)
        self.assertIn('data-icon="ExclamationTriangleIcon"', error)
        self.assertIn(
            "M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z",
            error,
        )
        self.assertIn(".status-loading", css)
        self.assertIn(".status-error", css)
        self.assertIn("color: rgb(var(--main-accent))", css)
        self.assertIn("width: 28px", css)
        self.assertIn("width: 40px", css)

    def test_progress_bar(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="progress-bar"', patterns)
        bars = html[html.index('data-pattern="progress-bar"') :]
        self.assertIn('class="progress-bar"', bars)
        for state in ("ok", "warn", "over"):
            self.assertIn(f'data-state="{state}"', bars)
        self.assertIn("56.5487", bars)
        self.assertIn("87.9646", bars)
        self.assertIn("stroke-dasharray", bars)
        self.assertIn("stroke-dashoffset", bars)
        home_main = html[html.index('class="home-main"') : html.index('data-pattern="tweet"')]
        self.assertIn("progress-bar", home_main)
        self.assertIn("composer-rule", home_main)
        self.assertIn('data-icon="PlusIcon"', home_main)
        self.assertIn("M12 4.5v15m7.5-7.5h-15", home_main)
        self.assertIn(".progress-bar", css)
        self.assertIn(".progress-bar[data-state=\"ok\"]", css)
        self.assertIn(".progress-bar[data-state=\"warn\"]", css)
        self.assertIn(".progress-bar[data-state=\"over\"]", css)
        self.assertIn("stroke: rgb(var(--main-accent))", css)
        self.assertIn("stroke: rgb(var(--accent-yellow))", css)
        self.assertIn("stroke: rgb(var(--accent-red))", css)
        self.assertIn("transform: rotate(-90deg)", css)
        self.assertIn("#B9CAD3", css)
        self.assertIn("#3E4144", css)

    def test_stats_empty(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="stats-empty"', patterns)
        empty = html[html.index('data-pattern="stats-empty"') :]
        self.assertIn('class="stats-empty"', empty)
        self.assertIn("@alice hasn't liked any Tweets", empty)
        self.assertIn("When they do, those Tweets will show up here.", empty)
        self.assertIn(".stats-empty", css)
        self.assertIn("max-width: 24rem", css)
        self.assertIn("font-size: 30px", css)
        self.assertIn("font-weight: 800", css)

    def test_user_hover_card(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="user-hover"', patterns)
        card = html[html.index('data-pattern="user-hover"') :]
        self.assertIn("user-hover-card", card)
        self.assertIn("user-hover-cover", card)
        self.assertIn("is-empty", card)
        self.assertIn("Follows you", card)
        self.assertIn("btn-follow", card)
        self.assertIn("user-follow-stats", card)
        self.assertIn(".user-hover-card", css)
        self.assertIn("width: 18rem", css)
        self.assertIn(".user-hover-host:hover .user-hover-card", css)
        self.assertIn("delay: 500ms", css)
        self.assertIn(".user-hover-cover.is-empty", css)
        self.assertIn("background: var(--reply-line)", css)
        self.assertIn(".user-follows-you", css)
        self.assertIn("rgb(var(--main-search-background))", css)
        self.assertIn("#65778633", css)

    def test_edit_profile_modal(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="edit-profile"', patterns)
        modal = html[html.index('data-pattern="edit-profile"') :]
        self.assertIn("Edit profile", modal)
        self.assertIn("Save", modal)
        self.assertIn("Switch to professional", modal)
        self.assertIn('data-icon="CameraIcon"', modal)
        self.assertIn(
            "M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z",
            modal,
        )
        self.assertIn('data-icon="ArrowPathIcon"', modal)
        self.assertIn("M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99", modal)
        self.assertIn('data-icon="ChevronRightIcon"', modal)
        self.assertIn("M8.25 4.5l7.5 7.5-7.5 7.5", modal)
        self.assertIn(".edit-profile", css)
        self.assertIn(".edit-profile-cover", css)
        self.assertIn("height: 144px", css)

    def test_username_modal(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="username-modal"', patterns)
        modal = html[html.index('data-pattern="username-modal"') :]
        self.assertIn("What should we call you?", modal)
        self.assertIn("Your @username is unique", modal)
        self.assertIn("Set username", modal)
        self.assertIn("Skip", modal)
        self.assertIn('data-icon="TwitterIcon"', modal)
        self.assertIn("M23.643 4.937c-.835.37-1.732.62-2.675.733", modal)
        self.assertIn(".username-modal", css)
        self.assertIn(".username-modal-main", css)
        self.assertIn(".username-modal-skip", css)

    def test_mobile_sidebar(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="mobile-sidebar"', patterns)
        drawer = html[html.index('data-pattern="mobile-sidebar"') :]
        self.assertIn("Account info", drawer)
        for label in (
            "Topics",
            "Bookmarks",
            "Lists",
            "Twitter Circle",
            "Settings and privacy",
            "Help center",
            "Display",
            "Log out",
        ):
            self.assertIn(label, drawer)
        self.assertIn('data-icon="ChatBubbleBottomCenterTextIcon"', drawer)
        self.assertIn(
            "M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z",
            drawer,
        )
        self.assertIn('data-icon="PaintBrushIcon"', drawer)
        self.assertIn("M9.53 16.122a3 3 0 00-5.78 1.128", drawer)
        self.assertIn('data-icon="ArrowRightOnRectangleIcon"', drawer)
        self.assertIn("M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5", drawer)
        self.assertIn(".mobile-sidebar", css)
        self.assertIn(".mobile-sidebar-panel", css)

    def test_reply_modal(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="reply-modal"', patterns)
        modal = html[html.index('data-pattern="reply-modal"') :]
        self.assertIn('role="dialog"', modal)
        self.assertIn("Tweet your reply", modal)
        self.assertIn("Replying to", modal)
        self.assertIn('class="composer"', modal)
        self.assertIn(".reply-modal", css)
        self.assertIn(".reply-modal-panel", css)

    def test_stats_modal(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        patterns = html[html.index('id="patterns"') :]
        self.assertIn('data-pattern="stats-modal"', patterns)
        modal = html[html.index('data-pattern="stats-modal"') :]
        self.assertIn("Liked by", modal)
        self.assertIn('data-icon="XMarkIcon"', modal)
        self.assertIn("M6 18L18 6M6 6l12 12", modal)
        self.assertIn("stats-empty", modal)
        self.assertIn(".stats-modal", css)
        self.assertIn(".stats-modal-header", css)

    def test_auth_landing_and_login_modal(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        landing = html[html.index('data-pattern="auth-landing"') :]
        self.assertIn("Happening now.", landing)
        self.assertIn("Continue with phone", landing)
        self.assertIn("Continue with Google", landing)
        self.assertIn("Continue with Apple", landing)
        self.assertIn("Email or username", landing)
        self.assertIn("btn-social", landing)
        self.assertIn("auth-field", landing)
        self.assertIn("btn-continue", landing)
        self.assertIn("auth-or", landing)
        self.assertIn("M24 9.5c3.54 0 6.71 1.22", landing)
        self.assertIn("M16.365 1.43c0 1.14", landing)
        modal = html[html.index('data-pattern="login-modal"') : html.index('data-pattern="signup-aside"')]
        self.assertIn("See what's happening", modal)
        self.assertIn("login-modal-backdrop", modal)
        self.assertIn("login-modal-panel", modal)
        self.assertIn('aria-label="Back"', modal)
        self.assertIn("M24 9.5c3.54 0 6.71 1.22", modal)
        self.assertIn("M16.365 1.43c0 1.14", modal)
        aside = html[html.index('data-pattern="signup-aside"') :]
        self.assertIn("Log in or sign up for X", aside)
        self.assertIn("Log in with username or email", aside)
        self.assertIn("M24 9.5c3.54 0 6.71 1.22", aside)
        self.assertIn("M15.75 6a3.75 3.75 0 11-7.5 0", aside)
        self.assertIn(".auth-landing", css)
        self.assertIn(".btn-social", css)
        self.assertIn(".auth-field", css)
        self.assertIn(".btn-continue", css)
        self.assertIn(".auth-or", css)
        self.assertIn(".login-modal", css)
        self.assertIn(".login-modal-panel", css)
        self.assertIn(".login-modal-backdrop", css)
        self.assertIn("box-shadow: 0 0 0 2px rgb(var(--main-accent))", css)

    def test_profile_mention_and_page_header(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        mention = html[html.index('data-pattern="profile-mention"') :]
        self.assertIn("Mention", mention)
        self.assertIn("btn-outline", mention)
        self.assertIn("btn-follow", mention)
        header = html[html.index('data-pattern="page-header"') :]
        self.assertIn("15.7K posts", header)
        self.assertIn("is-gold", header)
        self.assertIn('aria-label="Refresh"', header)
        self.assertIn('aria-label="Search"', header)
        self.assertIn(".btn-outline", css)
        self.assertIn(".page-header", css)
        self.assertIn(".tweet-verified.is-gold", css)
        self.assertIn("fill: rgb(var(--accent-yellow))", css)

    def test_quote_video_metrics_and_status(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        quote = html[html.index('data-pattern="quote-embed"') :]
        self.assertIn("quote-embed", quote)
        self.assertIn("Grok Bot", quote)
        self.assertIn("good bot", quote)
        video = html[html.index('data-pattern="video-media"') :]
        self.assertIn("video-play", video)
        self.assertIn("video-duration", video)
        self.assertIn("08:44:53", video)
        self.assertIn("M12.538 6.478", video)
        metrics = html[html.index('data-pattern="tweet-metrics"') :]
        self.assertIn('class="views"', metrics)
        self.assertIn('class="bookmark"', metrics)
        self.assertIn("699K", metrics)
        self.assertIn("M3 13.125C3 12.504", metrics)
        self.assertIn("M17.593 3.322", metrics)
        self.assertIn('class="status-detail" data-pattern="post-detail"', html)
        detail = html[html.index('data-pattern="post-detail"') :]
        self.assertIn("is-status", detail)
        self.assertIn("status-time", detail)
        self.assertIn("Tweet your reply", detail)
        self.assertIn(".quote-embed", css)
        self.assertIn(".video-media", css)
        self.assertIn(".video-play", css)
        self.assertIn(".video-duration", css)
        self.assertIn(".tweet-actions.is-wide", css)
        self.assertIn(".tweet-actions .views", css)
        self.assertIn(".tweet-actions .bookmark", css)
        self.assertIn(".status-detail", css)
        self.assertIn(".tweet-card.is-status", css)
        self.assertIn(".status-time", css)

    def test_logged_in_chrome(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        switcher = html[html.index('data-pattern="account-switcher"') : html.index('data-pattern="topic-tabs"')]
        self.assertIn("account-switcher-meta", switcher)
        self.assertIn("@alice", switcher)
        self.assertIn("M6.75 12a.75.75 0 11-1.5 0", switcher)
        topics = html[html.index('data-pattern="topic-tabs"') : html.index('data-pattern="news-aside"')]
        self.assertIn("For you", topics)
        self.assertIn("Following", topics)
        self.assertIn("Design", topics)
        self.assertIn("M12 4.5v15m7.5-7.5h-15", topics)
        self.assertIn("M19.5 8.25l-7.5 7.5-7.5-7.5", topics)
        news = html[html.index('data-pattern="news-aside"') : html.index('data-pattern="explore"')]
        self.assertIn("Today's News", news)
        self.assertIn("news-row", news)
        self.assertIn("Trending now · News", news)
        explore = html[html.index('data-pattern="explore"') : html.index('data-pattern="notifications"')]
        self.assertIn("Trending", explore)
        self.assertIn("Sports", explore)
        self.assertIn("Entertainment", explore)
        self.assertIn('aria-label="Settings"', explore)
        self.assertIn("M10.343 3.94", explore)
        notices = html[html.index('data-pattern="notifications"') : html.index('data-pattern="search-results"')]
        self.assertIn("All", notices)
        self.assertIn("Mentions", notices)
        self.assertIn("followed you", notices)
        self.assertIn("New post notifications", notices)
        self.assertIn("M19 7.5v3m0 0v3m0-3h3", notices)
        results = html[html.index('data-pattern="search-results"') : html.index('data-pattern="search-filters"')]
        self.assertIn('value="design"', results)
        self.assertIn("Top", results)
        self.assertIn("Latest", results)
        self.assertIn("People", results)
        self.assertIn("Media", results)
        self.assertIn("Lists", results)
        filters = html[html.index('data-pattern="search-filters"') :]
        self.assertIn("Search filters", filters)
        self.assertIn("From anyone", filters)
        self.assertIn("People you follow", filters)
        self.assertIn("Anywhere", filters)
        self.assertIn("Near you", filters)
        self.assertIn("M4.5 12.75l6 6 9-13.5", filters)
        self.assertIn(".tabs.is-scroll", css)
        self.assertIn(".tabs.is-five", css)
        self.assertIn(".topic-add", css)
        self.assertIn(".account-switcher", css)
        self.assertIn(".news-row", css)
        self.assertIn(".news-headline", css)
        self.assertIn(".explore-demo", css)
        self.assertIn(".notice-row", css)
        self.assertIn(".notice-mark", css)
        self.assertIn(".filter-row", css)
        self.assertIn(".filter-row.is-on", css)
        self.assertIn("color: rgb(var(--main-accent))", css)

    def test_messages_and_poll_chrome(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        inbox = html[html.index('data-pattern="messages"') : html.index('data-pattern="poll"')]
        self.assertIn("Chat", inbox)
        self.assertIn("Start a conversation", inbox)
        self.assertIn("New chat", inbox)
        self.assertIn("Search messages", inbox)
        self.assertIn("M20.7 11.7c0-4.48", inbox)
        poll = html[html.index('data-pattern="poll"') :]
        self.assertIn("Ask a question", poll)
        self.assertIn("Choice 1", poll)
        self.assertIn("Choice 2", poll)
        self.assertIn("Poll length", poll)
        self.assertIn("Remove poll", poll)
        self.assertIn("Everyone can reply", poll)
        self.assertIn("M6 5c-1.1 0-2 .895-2 2s.9 2 2 2", poll)
        self.assertIn("Grok", html)
        self.assertIn("Premium", html)
        self.assertIn('data-icon="XLogoIcon"', html)
        self.assertIn("M21.742 21.75l-7.563-11.179", html)
        self.assertIn("M23.643 4.937c-.835.37", html)
        self.assertIn(".messages-demo", css)
        self.assertIn(".messages-pane", css)
        self.assertIn(".poll-modal", css)
        self.assertIn(".poll-choice", css)
        self.assertIn(".poll-remove", css)
        self.assertIn("color: rgb(var(--accent-red))", css)

    # Responsive recipe — clone 62a9588 screens: xs 500, md 768, lg 1024, xl 1280.

    @staticmethod
    def media_block(css: str, query: str) -> str:
        """Concatenate every top-level block that opens with `query`."""
        blocks = []
        start = css.find(query)
        if start == -1:
            raise AssertionError(f"no block for {query}")
        while start != -1:
            depth = 0
            for i in range(start, len(css)):
                if css[i] == "{":
                    depth += 1
                elif css[i] == "}":
                    depth -= 1
                    if depth == 0:
                        blocks.append(css[start : i + 1])
                        break
            else:
                raise AssertionError(f"unterminated block for {query}")
            start = css.find(query, i + 1)
        return "\n".join(blocks)

    def test_leftover_fill(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn("See new posts", html)
        self.assertIn("Is this post relevant", html)
        self.assertIn("Search Communities", html)
        self.assertIn("Discover new Communities", html)
        self.assertIn("Create your Space", html)
        self.assertIn("Generate image", html)
        self.assertIn("Content disclosure", html)
        self.assertIn("Creator Studio", html)
        self.assertIn("Customize your view", html)
        self.assertIn("Join Twitter today.", html)
        self.assertIn("Log out @alice", html)
        self.assertIn("Help center", html)
        self.assertIn("Copy link to Tweet", html)
        self.assertIn("Remove Tweet from Bookmarks", html)
        self.assertIn("Follow @bob", html)
        self.assertIn('aria-label="Message"', html)
        self.assertIn("Follows you", html)
        self.assertIn("This account doesn’t exist", html)
        self.assertIn("Replies", html[html.index('data-pattern="status-counts"'):])
        self.assertIn("M3 2h18.61l-3.5 7 3.5 7H5v6H3V2zm2 12h13.38l-2.5-5 2.5-5H5v10z", html)
        self.assertIn("M10.059 2.593c1.175-.784", html)
        self.assertIn("M7.501 19.917L7.471 21H.472", html)
        self.assertIn("M10.5 6a7.5 7.5 0 107.5 7.5h-7.5V6z", html)
        self.assertIn(".new-posts", css)
        self.assertIn(".search-relevant", css)
        self.assertIn(".communities-demo", css)
        self.assertIn(".display-modal", css)
        self.assertIn(".auth-landing-clone", css)
        self.assertIn(".logout-popover", css)
        self.assertIn(".media-remove", css)
        self.assertIn(".status-counts", css)
        self.assertIn(".account-missing", css)
        self.assertIn(".stats-empty-art", css)
        self.assertIn("M10.5 6a7.5 7.5 0 107.5 7.5h-7.5V6z", html)

    def test_sidebar_icon_only_below_xl(self):
        sidebar = HTML[HTML.index('data-pattern="sidebar"') : HTML.index('class="home-main"')]
        self.assertIn('class="nav-label"', sidebar)
        self.assertIn('class="nav-feather"', sidebar)
        self.assertIn("M23 3c-6.62-.1-10.38 2.421", sidebar)  # FeatherIcon from showcase/icons
        block = self.media_block(SITE, "@media (max-width: 1279px)")
        self.assertIn(".sidebar-demo .nav-label", block)
        self.assertIn("display: none", block)
        self.assertIn("80px minmax(0, 576px) 384px", block)
        md = self.media_block(SITE, "@media (min-width: 768px) and (max-width: 1279px)")
        self.assertIn("96px", md)

    def test_aside_hidden_below_lg(self):
        block = self.media_block(SITE, "@media (max-width: 1023px)")
        self.assertIn(".aside-stack", block)
        self.assertIn("display: none", block)
        self.assertIn("80px minmax(0, 576px)", block)
        self.assertNotIn("384px", block)

    def test_sidebar_bottom_bar_below_xs(self):
        sidebar = HTML[HTML.index('data-pattern="sidebar"') : HTML.index('class="home-main"')]
        for hidden in ("HashtagIcon", "BookmarkIcon", "Bars3BottomLeftIcon"):
            self.assertRegex(sidebar, rf'data-nav-icon="{hidden}"[^>]*data-can-hide')
        self.assertNotRegex(sidebar, r'data-nav-icon="HomeIcon"[^>]*data-can-hide')
        block = self.media_block(SITE, "@media (max-width: 499px)")
        self.assertIn(".sidebar-demo", block)
        self.assertIn("position: fixed", block)
        self.assertIn("bottom: 0", block)
        self.assertIn("[data-can-hide]", block)
        self.assertIn(".sidebar-demo .logo-mark", block)
        self.assertIn("bottom: 72px", block)
        self.assertIn(".home-main", block)
        self.assertIn("border-left: 0", block)


if __name__ == "__main__":
    unittest.main()
