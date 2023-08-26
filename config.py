import json
import os
from datetime import datetime

from args import cmd_args

ROOT_DIR = os.getcwd()


with open(cmd_args.bot_data, 'r') as file:
    BOT_DATA = json.load(file)

# Bot
DEBUG = cmd_args.debug
API_TOKEN = BOT_DATA["debug" if DEBUG else "main"]['token']


# Yandex Music
YANDEX_MUSIC_TOKEN = BOT_DATA['yandex_music_token']


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
# Папки для логов
BOT_LOGS_DIR = os.path.join(ROOT_DIR, 'logs', 'bot')

# Папки логов данного процесса
PROCESS_LOG_DIR = os.path.join(BOT_LOGS_DIR, datetime.now().strftime('%Y-%m-%d %H-%M-%S'))


# Other
OWNER_CHAT_ID = 901655683
