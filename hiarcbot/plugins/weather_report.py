import os
import json
import requests

from slackbot.bot import respond_to

from hiarcbot import bot, sched

# 여의도 관측소
url = "http://apis.skplanetx.com/weather/summary?version=1&lat=37.5517109&lon=126.92611569999997&stnid=108"

header = {
    "x-skpop-userId": "kodingwarrior",
    "Accept-Language": "ko_KR",
    "Accept": "application/json",
    "appKey": os.getenv("WEATHER_PLANET_API_KEY")
}

def get_weather_summary():
    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        return 'error'

    weather_report = ""
    summary = json.loads(r.text)['weather']['summary']
    weather_report += "[오늘의 날씨]\n(%s / 최고 온도 : %s도 , 최저 온도 : %s도)\n" % \
                      (summary['today']['sky']['name'], summary['today']['temparature']['tmax'], summary['today']['temparature']['tmin'])

    weather_report += "[내일의 날씨]\n(%s / 최고 온도 : %s도 , 최저 온도 : %s도)\n" % \
                      (summary['tomorrow']['sky']['name'], summary['tomorrow']['temparature']['tmax'], summary['tomorrow']['temparature']['tmin'])

    weather_report += "[모레의 날씨]\n(%s / 최고 온도 : %s도 , 최저 온도 : %s도)\n" % \
                      (summary['dayAfterTomorrow']['sky']['name'], summary['dayAfterTomorrow']['temparature']['tmax'],
                       summary['dayAfterTomorrow']['temparature']['tmin'])

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
