import os
import re
import json
import requests

from slackbot.bot import respond_to

from hiarcbot import sched, bot
import slack_config

headers = {
    "Accept-Language": "ko_KR",
    "Accept": "application/json"
}

data = {
    "user_key": "hi-arc slackbot",
    "type": "text",
    "content": "오늘의 식단"
}

def get_schoolcafe_menu():
    r = requests.post(url=slack_config.SCHOOL_CAFE_API,
                      headers=headers, data=data)
    if r.status_code != 200:
        print("error")

    return json.loads(r.text)['message']['text']

@respond_to('^학식$', re.IGNORECASE)
def menu_reply(message):
    menu_summary = get_schoolcafe_menu()
    message.send(menu_summary)


@sched.scheduled_job('cron', hour=8, minute=0)
def notify_schoolcafe_menu():
    menu_summary = get_schoolcafe_menu()
    slack_client = getattr(bot, "_client", None)
    channel_id = slack_client.find_channel_by_name(u'gourmat')
    slack_client.send_message(channel_id, menu_summary)
