import random
from threading import Lock
from typing import TYPE_CHECKING

import rarfile

from sickchill.oldbeard.common import SD
from sickchill.oldbeard.numdict import NumDict

from .init_helpers import setup_gettext, sickchill_dir

if TYPE_CHECKING:
    from .movies import MovieList

setup_gettext()

dynamic_strings = (
    _("Drama"),
    _("Mystery"),
    _("Science-Fiction"),
    _("Crime"),
    _("Action"),
    _("Comedy"),
    _("Thriller"),
    _("Animation"),
    _("Family"),
    _("Fantasy"),
    _("Adventure"),
    _("Horror"),
    _("Film-Noir"),
    _("Sci-Fi"),
    _("Romance"),
    _("Sport"),
    _("War"),
    _("Biography"),
    _("History"),
    _("Music"),
    _("Western"),
    _("News"),
    _("Sitcom"),
    _("Reality-TV"),
    _("Documentary"),
    _("Game-Show"),
    _("Musical"),
    _("Talk-Show"),
    _("Science-Fiction"),
)

__INITIALIZED__ = {}
ADBA_CONNECTION = None
ADD_SHOWS_WITH_YEAR = False
ADD_SHOWS_WO_DIR = False
ADDIC7ED_PASS = None
ADDIC7ED_USER = None
AIRDATE_EPISODES = False
ALLOW_HIGH_PRIORITY = False
ALLOWED_EXTENSIONS = "srt,nfo,srr,sfv"
ANIDB_PASSWORD = None
ANIDB_USE_MYLIST = False
ANIDB_USERNAME = None
ANIME_DEFAULT = False
WHITELIST_DEFAULT = ""
BLACKLIST_DEFAULT = ""
ANIME_SPLIT_HOME = False
ANIME_SPLIT_HOME_IN_TABS = False
ANIMESUPPORT = False
ANON_REDIRECT = None
DEFAULT_ANON_REDIRECT = "https://anon.to/?"
API_KEY = None
API_ROOT = None
AUTO_UPDATE = False
AUTOPOSTPROCESSOR_FREQUENCY = None
autoPostProcessorScheduler = None
BACKLOG_DAYS = 7
BACKLOG_FREQUENCY = None
BACKLOG_MISSING_ONLY = False
backlogSearchScheduler = None
BOXCAR2_ACCESSTOKEN = None
BOXCAR2_NOTIFY_ONDOWNLOAD = False
BOXCAR2_NOTIFY_ONSNATCH = False
BOXCAR2_NOTIFY_ONSUBTITLEDOWNLOAD = False
CACHE_DIR = None
CALENDAR_ICONS = False
CALENDAR_UNPROTECTED = False
CF_AUTH_DOMAIN = ""
CF_POLICY_AUD = ""
CFG = None
CHECK_PROPERS_INTERVAL = None
CLIENT_WEB_URLS = {"torrent": "", "newznab": ""}
COMING_EPS_DISPLAY_PAUSED = False
COMING_EPS_DISPLAY_SNATCHED = False
COMING_EPS_LAYOUT = None
COMING_EPS_MISSED_RANGE = None
COMING_EPS_SORT = None
CONFIG_FILE = ""
CONFIG_VERSION = 8
CPU_PRESET = None
CREATE_MISSING_SHOW_DIRS = False
CREATEPID = False
CUSTOM_CSS = None
CUSTOM_CSS_PATH = None
DAEMON = None
DAILYSEARCH_FREQUENCY = 40
dailySearchScheduler = None
DATA_DIR = ""
DATE_PRESET = None
DBDEBUG = False
DEBUG = False
DEFAULT_AUTOPOSTPROCESSOR_FREQUENCY = 10
DEFAULT_BACKLOG_FREQUENCY = 21
DEFAULT_DAILYSEARCH_FREQUENCY = 40
DEFAULT_PAGE = "home"
DEFAULT_SHOWUPDATE_HOUR = random.randint(2, 4)
DEFAULT_UPDATE_FREQUENCY = 1
DELETE_FAILED = False
DELETE_NON_ASSOCIATED_FILES = False
DELRARCONTENTS = False
DEVELOPER = False
DISCORD_AVATAR_URL = "https://raw.githubusercontent.com/joelvaneenwyk/sickchill/main/sickchill/gui/slick/images/sickchill-sc.png"
DISCORD_NAME = "SickChill"
DISCORD_NOTIFY_DOWNLOAD = None
DISCORD_NOTIFY_SNATCH = None
DISCORD_NOTIFY_SUBTITLEDOWNLOAD = None
DISCORD_TTS = False
DISCORD_WEBHOOK = None
DISPLAY_ALL_SEASONS = True
DISPLAY_SHOW_SPECIALS = False
DOWNLOAD_PROPERS = False
DOWNLOAD_URL = None
EMAIL_FROM = None
EMAIL_HOST = None
EMAIL_LIST = None
EMAIL_NOTIFY_ONDOWNLOAD = False
EMAIL_NOTIFY_ONPOSTPROCESS = False
EMAIL_NOTIFY_ONSNATCH = False
EMAIL_NOTIFY_ONSUBTITLEDOWNLOAD = False
EMAIL_PASSWORD = None
EMAIL_PORT = 25
EMAIL_SUBJECT = None
EMAIL_TLS = False
EMAIL_USER = None
EMBEDDED_SUBTITLES_ALL = False
EMBY_APIKEY = None
EMBY_HOST = None
ENABLE_HTTPS = False
ENCRYPTION_SECRET = None
ENCRYPTION_VERSION = 0
ENDED_SHOWS_UPDATE_INTERVAL = 7
EP_DEFAULT_DELETED_STATUS = None
events = None
EXTRA_SCRIPTS = []
FANART_API_KEY = "9b3afaf26f6241bdb57d6cc6bd798da7"
FANART_BACKGROUND = None
FANART_BACKGROUND_OPACITY = None
FILE_TIMESTAMP_TIMEZONE = None
FLARESOLVERR_URI = ""
FREEMOBILE_APIKEY = ""
FREEMOBILE_ID = ""
FREEMOBILE_NOTIFY_ONDOWNLOAD = False
FREEMOBILE_NOTIFY_ONSNATCH = False
FREEMOBILE_NOTIFY_ONSUBTITLEDOWNLOAD = False
FUZZY_DATING = False
gh = None
GIT_ORG = "SickChill"
GIT_REPO = "SickChill"
GIT_TOKEN = None
GIT_USERNAME = None
GOTIFY_AUTHORIZATIONTOKEN = None
GOTIFY_HOST = None
GOTIFY_NOTIFY_ONDOWNLOAD = False
GOTIFY_NOTIFY_ONSNATCH = False
GOTIFY_NOTIFY_ONSUBTITLEDOWNLOAD = False
GROWL_HOST = ""
GROWL_NOTIFY_ONDOWNLOAD = False
GROWL_NOTIFY_ONSNATCH = False
GROWL_NOTIFY_ONSUBTITLEDOWNLOAD = False
GROWL_PASSWORD = None
GUI_LANG = None
GUI_NAME = None
HANDLE_REVERSE_PROXY = False
HISTORY_LAYOUT = None
HISTORY_LIMIT = 0
HOME_LAYOUT = None
HTTPS_CERT = None
HTTPS_KEY = None
IGNORE_BROKEN_SYMLINKS = False
IGNORE_WORDS = "german,french,core2hd,dutch,swedish,reenc,MrLss"
IGNORED_SUBS_LIST = "dk,fin,heb,kor,nor,nordic,pl,swe"
IMAGE_CACHE = None
INDEXER_DEFAULT = 1
INDEXER_DEFAULT_LANGUAGE = None
INDEXER_TIMEOUT = None
INIT_LOCK = Lock()
ITASA_PASS = None
ITASA_USER = None
JOIN_APIKEY = ""
JOIN_ID = ""
JOIN_NOTIFY_ONDOWNLOAD = False
JOIN_NOTIFY_ONSNATCH = False
JOIN_NOTIFY_ONSUBTITLEDOWNLOAD = False
KEEP_PROCESSED_DIR = False
KODI_ALWAYS_ON = True
KODI_HOST = ""
KODI_NOTIFY_ONDOWNLOAD = False
KODI_NOTIFY_ONSNATCH = False
KODI_NOTIFY_ONSUBTITLEDOWNLOAD = False
KODI_PASSWORD = None
KODI_UPDATE_FULL = False
KODI_UPDATE_LIBRARY = False
KODI_UPDATE_ONLYFIRST = False
KODI_USERNAME = None
LAUNCH_BROWSER = False
LEGENDASTV_PASS = None
LEGENDASTV_USER = None
LIBNOTIFY_NOTIFY_ONDOWNLOAD = False
LIBNOTIFY_NOTIFY_ONPOSTPROCESS = False
LIBNOTIFY_NOTIFY_ONSNATCH = False
LIBNOTIFY_NOTIFY_ONSUBTITLEDOWNLOAD = False
LOCALHOST_IP = None
LOG_DIR = None
LOG_NR = 5
LOG_SIZE = 10.0
LOGO_URL = "https://sickchill.github.io/images/ico/favicon-64.png"
MATRIX_API_TOKEN = None
MATRIX_NOTIFY_DOWNLOAD = None
MATRIX_NOTIFY_SNATCH = None
MATRIX_NOTIFY_SUBTITLEDOWNLOAD = None
MATRIX_ROOM = None
MATRIX_SERVER = None
MESSAGES_LOCK = Lock()
METADATA_KODI = None
METADATA_MEDE8ER = None
METADATA_MEDIABROWSER = None
metadata_provider_dict = {}
METADATA_PS3 = None
METADATA_TIVO = None
METADATA_WDTV = None
MIN_AUTOPOSTPROCESSOR_FREQUENCY = 1
MIN_BACKLOG_FREQUENCY = 10
MIN_DAILYSEARCH_FREQUENCY = 10
MIN_UPDATE_FREQUENCY = 1
MOVE_ASSOCIATED_FILES = False
MY_ARGS = []
MY_FULLNAME = None
MY_NAME = None
NAMING_ABD_PATTERN = None
NAMING_ANIME = None
NAMING_ANIME_MULTI_EP = False
NAMING_ANIME_PATTERN = None
NAMING_CUSTOM_ABD = False
NAMING_CUSTOM_ANIME = False
NAMING_CUSTOM_SPORTS = False
NAMING_FORCE_FOLDERS = False
NAMING_MULTI_EP = False
NAMING_PATTERN = None
NAMING_SPORTS_PATTERN = None
NAMING_STRIP_YEAR = False
NAMING_NO_BRACKETS = False
NEWS_LAST_READ = None
NEWS_LATEST = None
NEWS_UNREAD = 0
NEWS_URL = "https://sickchill.github.io/sickchill-news/news.md"
NEWZBIN = False
NEWZBIN_PASSWORD = None
NEWZBIN_USERNAME = None
NEWZNAB_DATA = None
newznab_provider_list = []
NFO_RENAME = True
NMA_API = None
NMA_NOTIFY_ONDOWNLOAD = False
NMA_NOTIFY_ONSNATCH = False
NMA_NOTIFY_ONSUBTITLEDOWNLOAD = False
NMA_PRIORITY = 0
NMJ_DATABASE = None
NMJ_HOST = None
NMJ_MOUNT = None
NMJv2_DATABASE = None
NMJv2_DBLOC = None
NMJv2_HOST = None
NO_DELETE = False
NO_LGMARGIN = False
NO_RESIZE = False
NO_RESTART = False
notificationsTaskScheduler = None
NOTIFY_ON_LOGIN = False
NOTIFY_ON_LOGGED_ERROR = False
NOTIFY_ON_UPDATE = False
NZB_DIR = None
NZB_METHOD = None
NZBGET_CATEGORY = None
NZBGET_CATEGORY_ANIME = None
NZBGET_CATEGORY_ANIME_BACKLOG = None
NZBGET_CATEGORY_BACKLOG = None
NZBGET_HOST = None
NZBGET_PASSWORD = None
NZBGET_PRIORITY = 100
NZBGET_USE_HTTPS = False
NZBGET_USERNAME = None
NZBS = False
NZBS_HASH = None
NZBS_UID = None
OMGWTFNZBS = False
OMGWTFNZBS_APIKEY = None
OMGWTFNZBS_USERNAME = None
OPENSUBTITLES_PASS = None
OPENSUBTITLES_USER = None
PID = None
PIDFILE = ""
PLEX_CLIENT_HOST = None
PLEX_CLIENT_PASSWORD = None
PLEX_CLIENT_USERNAME = None
PLEX_NOTIFY_ONDOWNLOAD = False
PLEX_NOTIFY_ONSNATCH = False
PLEX_NOTIFY_ONSUBTITLEDOWNLOAD = False
PLEX_SERVER_HOST = None
PLEX_SERVER_HTTPS = None
PLEX_SERVER_PASSWORD = None
PLEX_SERVER_TOKEN = None
PLEX_SERVER_USERNAME = None
PLEX_UPDATE_LIBRARY = False
POSTER_SORTBY = None
POSTER_SORTDIR = None
POSTPONE_IF_SYNC_FILES = True
postProcessorTaskScheduler = None
PREFER_WORDS = ""
PROCESS_AUTOMATICALLY = False
PROCESS_METHOD = None
PROCESSOR_FOLLOW_SYMLINKS = False
PROG_DIR = sickchill_dir
properFinderScheduler = None
PROVIDER_ORDER = []
providerList = []
PROWL_API = None
PROWL_MESSAGE_TITLE = "SickChill"
PROWL_NOTIFY_ONDOWNLOAD = False
PROWL_NOTIFY_ONSNATCH = False
PROWL_NOTIFY_ONSUBTITLEDOWNLOAD = False
PROWL_PRIORITY = 0
PROXY_INDEXERS = False
PROXY_SETTING = None
PUSHALOT_AUTHORIZATIONTOKEN = None
PUSHALOT_NOTIFY_ONDOWNLOAD = False
PUSHALOT_NOTIFY_ONSNATCH = False
PUSHALOT_NOTIFY_ONSUBTITLEDOWNLOAD = False
PUSHBULLET_API = None
PUSHBULLET_CHANNEL = None
PUSHBULLET_DEVICE = None
PUSHBULLET_NOTIFY_ONDOWNLOAD = False
PUSHBULLET_NOTIFY_ONSNATCH = False
PUSHBULLET_NOTIFY_ONSUBTITLEDOWNLOAD = False
PUSHOVER_APIKEY = None
PUSHOVER_DEVICE = None
PUSHOVER_NOTIFY_ONDOWNLOAD = False
PUSHOVER_NOTIFY_ONSNATCH = False
PUSHOVER_NOTIFY_ONSUBTITLEDOWNLOAD = False
PUSHOVER_PRIORITY = 0
PUSHOVER_SOUND = None
PUSHOVER_USERKEY = None
PYTIVO_HOST = ""
PYTIVO_NOTIFY_ONDOWNLOAD = False
PYTIVO_NOTIFY_ONSNATCH = False
PYTIVO_NOTIFY_ONSUBTITLEDOWNLOAD = False
PYTIVO_SHARE_NAME = ""
PYTIVO_TIVO_NAME = ""
PYTIVO_UPDATE_LIBRARY = False
QUALITY_DEFAULT = SD
RANDOMIZE_PROVIDERS = False
RENAME_EPISODES = False
REQUIRE_WORDS = ""
ROCKETCHAT_ICON_EMOJI = None
ROCKETCHAT_NOTIFY_DOWNLOAD = None
ROCKETCHAT_NOTIFY_SNATCH = None
ROCKETCHAT_NOTIFY_SUBTITLEDOWNLOAD = None
ROCKETCHAT_WEBHOOK = None
ROOT_DIRS = None
SAB_APIKEY = None
SAB_CATEGORY = None
SAB_CATEGORY_ANIME = None
SAB_CATEGORY_ANIME_BACKLOG = None
SAB_CATEGORY_BACKLOG = None
SAB_FORCED = False
SAB_HOST = ""
SAB_PASSWORD = None
SAB_USERNAME = None
SCENE_DEFAULT = False
searchQueueScheduler = None
SEASON_FOLDERS_DEFAULT = False
showList = []
showQueueScheduler = None
SHOWS_RECENT = []
SHOWUPDATE_HOUR = None
showUpdateScheduler = None
SICKCHILL_BACKGROUND = None
SICKCHILL_BACKGROUND_PATH = None
SITE_MESSAGES = {}
SKIP_REMOVED_FILES = False
SLACK_ICON_EMOJI = None
SLACK_NOTIFY_DOWNLOAD = None
SLACK_NOTIFY_SNATCH = None
SLACK_NOTIFY_SUBTITLEDOWNLOAD = None
SLACK_WEBHOOK = None
MATTERMOST_ICON_EMOJI = None
MATTERMOST_NOTIFY_DOWNLOAD = None
MATTERMOST_NOTIFY_SNATCH = None
MATTERMOST_NOTIFY_SUBTITLEDOWNLOAD = None
MATTERMOST_WEBHOOK = None
MATTERMOST_USERNAME = None
MATTERMOSTBOT_ICON_EMOJI = None
MATTERMOSTBOT_AUTHOR = None
MATTERMOSTBOT_NOTIFY_DOWNLOAD = None
MATTERMOSTBOT_NOTIFY_SNATCH = None
MATTERMOSTBOT_NOTIFY_SUBTITLEDOWNLOAD = None
MATTERMOSTBOT_URL = None
MATTERMOSTBOT_TOKEN = None
MATTERMOSTBOT_CHANNEL = None
SOCKET_TIMEOUT = None
SORT_ARTICLE = False
GRAMMAR_ARTICLES = "the|a|an"
SSL_VERIFY = True
started = {}
STATUS_DEFAULT = None
STATUS_DEFAULT_AFTER = None
SUBSCENTER_PASS = None
SUBSCENTER_USER = None
SUBTITLES_DEFAULT = False
SUBTITLES_DIR = ""
SUBTITLES_EXTRA_SCRIPTS = []
SUBTITLES_FINDER_FREQUENCY = 1
SUBTITLES_HEARING_IMPAIRED = False
SUBTITLES_HISTORY = False
SUBTITLES_INCLUDE_SPECIALS = True
SUBTITLES_KEEP_ONLY_WANTED = False
SUBTITLES_LANGUAGES = []
SUBTITLES_MULTI = False
SUBTITLES_PERFECT_MATCH = False
SUBTITLES_SERVICES_ENABLED = []
SUBTITLES_SERVICES_LIST = []
subtitlesFinderScheduler = None
SYNC_FILES = "!sync,lftp-pget-status,bts,!qb"
SYNOLOGY_DSM_HOST = None
SYNOLOGY_DSM_PASSWORD = None
SYNOLOGY_DSM_PATH = None
SYNOLOGY_DSM_USERNAME = None
SYNOLOGYNOTIFIER_NOTIFY_ONDOWNLOAD = False
SYNOLOGYNOTIFIER_NOTIFY_ONSNATCH = False
SYNOLOGYNOTIFIER_NOTIFY_ONSUBTITLEDOWNLOAD = False
TELEGRAM_APIKEY = ""
TELEGRAM_ID = ""
TELEGRAM_NOTIFY_ONDOWNLOAD = False
TELEGRAM_NOTIFY_ONSNATCH = False
TELEGRAM_NOTIFY_ONSUBTITLEDOWNLOAD = False
THEME_NAME = None
TIME_PRESET = None
TIME_PRESET_W_SECONDS = None
TIMEZONE_DISPLAY = None
TMDB_API_KEY = "edc5f123313769de83a71e157758030b"
TORRENT_AUTH_TYPE = "none"
TORRENT_DIR = None
TORRENT_HIGH_BANDWIDTH = False
TORRENT_HOST = ""
TORRENT_LABEL = ""
TORRENT_LABEL_ANIME = ""
TORRENT_METHOD = None
TORRENT_PASSWORD = None
TORRENT_PATH = ""
TORRENT_PATH_INCOMPLETE = ""
TORRENT_PAUSED = False
TORRENT_RPCURL = "transmission"
TORRENT_SEED_TIME = None
TORRENT_USERNAME = None
TORRENT_VERIFY_CERT = False
torrent_rss_provider_list = []
TRACKERS_LIST = "udp://coppersurfer.tk:6969/announce,udp://open.demonii.com:1337,"
TRACKERS_LIST += "udp://9.rarbg.to:2710/announce"
TRACKERS_LIST += "udp://exodus.desync.com:6969,udp://9.rarbg.me:2710/announce,"
TRACKERS_LIST += "udp://glotorrents.pw:6969/announce,udp://tracker.openbittorrent.com:80/announce,"
TRACKERS_LIST += "udp://tracker.opentrackr.org:1337/announce,udp://tracker.internetwarriors.net:1337"
TRAKT_ACCESS_TOKEN = None
# TRAKT_API_KEY = 'd4161a7a106424551add171e5470112e4afdaf2438e6ef2fe0548edc75924868'
TRAKT_API_KEY = "5c65f55e11d48c35385d9e8670615763a605fad28374c8ae553a7b7a50651ddd"
TRAKT_API_SECRET = "b53e32045ac122a445ef163e6d859403301ffe9b17fb8321d428531b69022a82"
TRAKT_API_URL = "https://api-v2launch.trakt.tv/"
TRAKT_BLACKLIST_NAME = None
TRAKT_DEFAULT_INDEXER = None
TRAKT_METHOD_ADD = None
TRAKT_OAUTH_URL = "https://trakt.tv/"
TRAKT_PIN_URL = "https://trakt.tv/pin/4562"
TRAKT_REFRESH_TOKEN = None
TRAKT_REMOVE_SERIESLIST = False
TRAKT_REMOVE_SHOW_FROM_SICKCHILL = False
TRAKT_REMOVE_WATCHLIST = False
TRAKT_START_PAUSED = False
TRAKT_SYNC = False
TRAKT_SYNC_REMOVE = False
TRAKT_SYNC_WATCHLIST = False
TRAKT_TIMEOUT = None
TRAKT_USE_RECOMMENDED = False
TRAKT_USERNAME = None
traktCheckerScheduler = None
TRASH_REMOVE_SHOW = False
TRASH_ROTATE_LOGS = False
TRIM_ZERO = False
TV_DOWNLOAD_DIR = None
TVDB_USER = None
TVDB_USER_KEY = None
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_NOTIFY_ONDOWNLOAD = False
TWILIO_NOTIFY_ONSNATCH = False
TWILIO_NOTIFY_ONSUBTITLEDOWNLOAD = False
TWILIO_PHONE_SID = ""
TWILIO_TO_NUMBER = ""
TWITTER_DMTO = None
TWITTER_NOTIFY_ONDOWNLOAD = False
TWITTER_NOTIFY_ONSNATCH = False
TWITTER_NOTIFY_ONSUBTITLEDOWNLOAD = False
TWITTER_PASSWORD = None
TWITTER_PREFIX = None
TWITTER_USEDM = False
TWITTER_USERNAME = None
UNAR_TOOL = rarfile.UNAR_TOOL
UNPACK_DISABLED = 0
UNPACK = UNPACK_DISABLED
UNPACK_DIR = ""
UNPACK_PROCESS_CONTENTS = 1
UNPACK_PROCESS_INTACT = 2
UNRAR_TOOL = rarfile.UNRAR_TOOL
UPDATE_FREQUENCY = None
USE_ANIDB = False
USE_BOXCAR2 = False
USE_DISCORD = False
USE_EMAIL = False
USE_EMBY = False
USE_FAILED_DOWNLOADS = False
USE_FREE_SPACE_CHECK = True
USE_FREEMOBILE = False
USE_GOTIFY = False
USE_GROWL = False
USE_ICACLS = True
USE_JOIN = False
USE_KODI = False
USE_LIBNOTIFY = False
USE_LISTVIEW = False
USE_MATRIX = False
USE_NMA = False
USE_NMJ = False
USE_NMJv2 = False
USE_NZBS = False
USE_PLEX_CLIENT = False
USE_PLEX_SERVER = False
USE_PROWL = False
USE_PUSHALOT = False
USE_PUSHBULLET = False
USE_PUSHOVER = False
USE_PYTIVO = False
USE_ROCKETCHAT = False
USE_SLACK = False
USE_MATTERMOST = False
USE_MATTERMOSTBOT = False
USE_SUBTITLES = False
USE_SYNOINDEX = False
USE_SYNOLOGYNOTIFIER = False
USE_TELEGRAM = False
USE_TORRENTS = False
USE_TRAKT = False
USE_TWILIO = False
USE_TWITTER = False
USENET_RETENTION = None
CACHE_RETENTION = 30
SHOW_SKIP_OLDER = 30
VERSION_NOTIFY = False
versionCheckScheduler = None
WEB_COOKIE_SECRET = None
WEB_HOST = None
WEB_IPV6 = False
WEB_LOG = False
WEB_PASSWORD = None
WEB_PORT = None
WEB_ROOT = None
WEB_USE_GZIP = True
WEB_USERNAME = None
WINDOWS_SHARES = {}

movie_list: "MovieList" = None


def get_backlog_cycle_time():
    # backlog timer multiple of daily frequency and ensure multiple per mako 'step="60"'
    cycle_time = ((DAILYSEARCH_FREQUENCY * 2) // 60) * 60
    return max([cycle_time, 720])


unpackStrings = NumDict(
    {
        UNPACK_DISABLED: _("Ignore (do not process contents)"),
        UNPACK_PROCESS_CONTENTS: _("Unpack (process contents)"),
        UNPACK_PROCESS_INTACT: _("Treat as video (process archive as-is)"),
    }
)
