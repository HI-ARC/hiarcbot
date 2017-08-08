import re

from slackbot.bot import respond_to

from hiarcbot import bot

@respond_to('has joined this channel$', re.IGNORECASE)
def hello_message(message):
    username = message.username
    msg = "%s 님 안녕하세요! 자기소개 부탁드려요~" % username
    message.send(msg)
