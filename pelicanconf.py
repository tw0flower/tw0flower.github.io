AUTHOR = "tw0flower"
SITENAME = "tw0flower"
SITEURL = "https://tw0flower.github.io"
TIMEZONE = "Asia/Tokyo"
DEFAULT_LANG = "en"
PATH = "content"

DEFAULT_METADATA = {
    "status": "draft",
}

THEME_STATIC_PATHS = ["static"]
PLUGINS = [
    "pelican.plugins.neighbors",
    "pelican.plugins.webassets",
]
MARKDOWN = {"extension_configs": {"markdown.extensions.codehilite": {"linenums": None}}}

PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"

ARCHIVES_SAVE_AS = "archive/index.html"
YEAR_ARCHIVE_SAVE_AS = "{date:%Y}/index.html"
MONTH_ARCHIVE_SAVE_AS = "{date:%Y}/{date:%m}/index.html"

THEME = "themes/Pneumatic"
ICONS_PATH = "images/icons"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
RSS_FEED_SUMMARY_ONLY = True

LOCALE = ('en_US', 'fr_FR')

BIO_TEXT = "Devops Engineer, Python developer and general computer handyman"
FOOTER_TEXT = 'Built with <a href="https://github.com/getpelican/pelican">Pelican</a> using the <a href="https://github.com/iKevinY/pneumatic">Pneumatic</a> theme.'

TWITTER_USERNAME = "tw0flower_"
# MASTODON_URL = "https://tech.lgbt/@tw0flower"

SOCIAL_ICONS = [
    ("https://github.com/tw0flower", "GitHub", "fa-github"),
    ("https://twitter.com/tw0flower_", "Twitter", "fa-twitter"),
    ("https://tech.lgbt/@tw0flower", "Mastodon", "fa-comments-o"),
    ("/atom.xml", "Atom Feed", "fa-solid fa-rss"),
]

SIDEBAR_LINKS = [
    '<a href="/pages/about/">About</a>',
    '<a href="/archive/">Archive</a>',
]
