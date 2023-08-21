import argparse

parser = argparse.ArgumentParser(description='Telegram bot')
parser.add_argument('-bot_data', type=str, required=True, help='Path to file with base bot data (like token and etc.)')
parser.add_argument('--debug', type=bool, required=False, default=True, help='Debug mode')
cmd_args = parser.parse_args()
