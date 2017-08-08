import os

API_TOKEN= os.getenv("HIARC_SLACK_API_TOKEN")

DEFAULT_REPLY = "봇 테스트는 #bot-test 에서 해주세요"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

PLUGINS = [
    'hiarcbot.plugins.help',
    'hiarcbot.plugins.ebook_notify',
    'hiarcbot.plugins.say_hello'
]
