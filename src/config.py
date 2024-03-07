import json
import os
from datetime import datetime

from args import cmd_args
from teleapi.core.project_state import ProjectState
from teleapi.core.utils.collections import DotDict

# Root
ROOT_DIR = os.getcwd()

# Bot
STATE = cmd_args.state
DEBUG = STATE is ProjectState.DEBUG

# Secrets
SECRETS_DIR = os.path.join(ROOT_DIR, 'secrets')

# Configs
CONFIGS_DIR = os.path.join(SECRETS_DIR, 'configs')
DEBUG_SECRETS_PATH = os.path.join(CONFIGS_DIR, 'dev.json')
PRODUCTION_SECRETS_PATH = os.path.join(CONFIGS_DIR, 'prod.json')
SECRET_CONFIG_PATH = DEBUG_SECRETS_PATH if DEBUG else PRODUCTION_SECRETS_PATH

# YTDLP
YTDLP_OPTIONS = {
    'format': '22/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best/bestaudio',
    'noplaylist': True,
    "quiet": True
}

# YouTube formats
AVAILABLE_YOUTUBE_SOUND_FORMAT = "140"
AVAILABLE_YOUTUBE_VIDEO_FORMAT = "22"

# Logs
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
CURRENT_PROCESS_LOGS_DIR = os.path.join(LOGS_DIR, datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
BOT_DEBUG_LOG_FILE_PATH = os.path.join(CURRENT_PROCESS_LOGS_DIR, 'debug.log')
BOT_INFO_LOG_FILE_PATH = os.path.join(CURRENT_PROCESS_LOGS_DIR, 'info.log')

# Resources
RESOURCES_FOLDER = os.path.join(ROOT_DIR, "src", "resources")
STRINGS_FOLDER = os.path.join(RESOURCES_FOLDER, "strings")
STRINGS_PATH = os.path.join(STRINGS_FOLDER, 'strings.json')
STRINGS: DotDict

with open(STRINGS_PATH, "r", encoding="utf-8") as file:
    STRINGS = DotDict(json.load(file))


# Other
OWNER_CHAT_ID = 901655683
