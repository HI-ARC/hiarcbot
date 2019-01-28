import re

from slackbot.bot import respond_to, default_reply

from hiarcbot import bot

help_dict = {
    "ebook": "PacktPub 에서 매일 무료로 배포하는 EBook을 확인",
    "BOJ XXXX": "Baekjoon Online Judge 문제 빠른 조회",
    "백준 YYYY번 문제": "위와 동일",
}


@respond_to('^help$', re.IGNORECASE)
def help(message):
    msg = "[ HI-ARC Bot 명령어 도움말 ]\n"
    for k, v in help_dict.items():
        msg += "%s : %s\n" % (k, v)
    message.send(msg)


@default_reply
def default_reply(message):
    channel_body = getattr(message.channel, "_body", None)
    if channel_body['name'] != 'etc_test':
        slack_client = getattr(bot, "_client", None)
        channel_id = slack_client.find_channel_by_name('etc_test')
        message.send("봇 테스트는 <#%s|%s> 에서 해주세요" % (channel_id, "etc_test"))
        return
