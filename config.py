import json
from args import cmd_args

with open(cmd_args.bot_data, 'r') as file:
    BOT_DATA = json.load(file)

# Bot
DEBUG = cmd_args.debug
API_TOKEN = BOT_DATA['token']

# Yandex Music
YANDEX_MUSIC_TOKEN = BOT_DATA['yandex_music_token']

# YTDLP
YTDLP_OPTIONS = {
    'format': '22/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best/bestaudio',
    'noplaylist': True,
    "quiet": True
}

AVAILABLE_YOUTUBE_SOUND_FORMAT = "140"
AVAILABLE_YOUTUBE_VIDEO_FORMAT = "22"
