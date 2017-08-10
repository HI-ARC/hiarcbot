import os
import re
import json
import requests

from slackbot.bot import respond_to

from hiarcbot import bot, sched
import slack_config

# 여의도 관측소
url = "http://apis.skplanetx.com/weather/summary?version=1&lat=37.5517109&lon=126.92611569999997&stnid=108"

headers = {
    "x-skpop-userId": "kodingwarrior",
    "Accept-Language": "ko_KR",
    "Accept": "application/json",
    "appKey": slack_config.WEATHER_PLANET_API_KEY
}

def weather_status_with_emoji(s):
    if s=='SKY_M01':
        return "맑음 :sunny:"
    elif s=='SKY_M02':
        return "구름조금 :sun_small_cloud:"
    elif s=='SKY_M03':
        return "구름많음 :sun_behind_cloud:"
    elif s=='SKY_M04':
        return "흐림 :cloud:" 
    elif s=='SKY_M05':
        return "비 :rain_cloud:"
    elif s=='SKY_M06':
        return "눈 :snow_cloud:"
    elif s=='SKY_M07':
        return "비 또는 눈 :rain_cloud: :snow_cloud:"
    else:
        return ":sunglasses:"

def get_weather_summary():
    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        return 'error'

    weather_report = ""
    summary = json.loads(r.text)['weather']['summary'][0]
    weather_report += "[오늘의 날씨]\n(%s / 최저 온도 : %s도 , 최고 온도 : %s도)\n\n" % \
                      (weather_status_with_emoji(summary['today']['sky']['code']),
                       summary['today']['temperature']['tmin'], summary['today']['temperature']['tmax'])

    weather_report += "[내일의 날씨]\n(%s / 최저 온도 : %s도 , 최고 온도 : %s도)\n\n" % \
                      (weather_status_with_emoji(summary['tomorrow']['sky']['code']),
                       summary['tomorrow']['temperature']['tmin'], summary['tomorrow']['temperature']['tmax'])

    weather_report += "[모레의 날씨]\n(%s / 최저 온도 : %s도 , 최고 온도 : %s도)\n" % \
                      (weather_status_with_emoji(summary['dayAfterTomorrow']['sky']['code']),
                       summary['dayAfterTomorrow']['temperature']['tmin'],
                       summary['dayAfterTomorrow']['temperature']['tmax'])

    return weather_report

@respond_to('^날씨$', re.IGNORECASE)
def help(message):
    weather_report = get_weather_summary()
    message.send(weather_report)


@sched.scheduled_job('cron', hour=7, minute=0)
def notify_to_general_weather_summary():
    weather_report = get_weather_summary()
    slack_client = getattr(bot, "_client", None)
    channel_id = slack_client.find_channel_by_name(u'_잡담')
    slack_client.send_message(channel_id, weather_report)
