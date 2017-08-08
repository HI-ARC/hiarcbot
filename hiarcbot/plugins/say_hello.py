import re

from slackbot.bot import listen_to


@listen_to("has joined the channel")
def hello_message(message):
    channel_body = getattr(message.channel, "_body", None)
    if channel_body['name'] == u'_잡담':
        username = u'<@{}>'.format(message._get_user_id())
        msg = "%s 님 안녕하세요! 자기소개 부탁드려요~ @_@" % username
        message.send(msg)
