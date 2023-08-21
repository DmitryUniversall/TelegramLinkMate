import json
from args import cmd_args

with open(cmd_args.bot_data, 'r') as file:
    BOT_DATA = json.load(file)

DEBUG = cmd_args.debug
API_TOKEN = BOT_DATA['token']
