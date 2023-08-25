import argparse

parser = argparse.ArgumentParser(description='Telegram bot')
parser.add_argument('-bot_data', required=True, help='Path to file with base bot data (like token and etc.)')
parser.add_argument('--debug', default=False, action=argparse.BooleanOptionalAction)

cmd_args = parser.parse_args()
