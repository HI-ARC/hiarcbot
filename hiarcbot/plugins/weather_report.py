import re
import requests
import operator

import pyowm

from slackbot.bot import respond_to

from hiarcbot import bot, sched
import slack_config

API_KEY = slack_config.OPEN_WEATHER_API_KEY

'''
def sky_code_to_message_with_emoji(code):
    mapping = {
        '01': '맑음 :sunny:',
        '02': '구름조금 :sun_small_cloud:',
        '03': '구름많음 :sun_behind_cloud:',
        '04': '흐림 :cloud:',
        '05': '비 :rain_cloud:',
        '06': '눈 :snow_cloud:',
        '07': '비 또는 눈 :rain_cloud: :snow_cloud:',
    }
    # SKY_M04 -> 04
    status = code[-2:]
    msg = mapping.get(status, ':sunglasses:')
    return msg
'''

def get_weather_summary():
    f = open('/tmp/weather_report', 'r')
    weather_report = f.read()
    f.close()
    
    return weather_report


@respond_to('^날씨$', re.IGNORECASE)
def help(message):
    weather_report = get_weather_summary()
    message.send(weather_report)

@respond_to('^날씨요청$', re.IGNORECASE)
def request_weather(message):
    save_weather_report()

@sched.scheduled_job('cron', hour=0, minute=0)
def save_weather_report():
    weather_location = 'Yongsan,KR'

    owm = pyowm.OWM(API_KEY)
    fc = owm.three_hours_forecast(weather_location)
    f = fc.get_forecast()

    weathers = f.get_weathers()[:8]

    status_frequency = {}
    temps = []
    status_arr = []
    
    for w in weathers:
        temps.append(w.get_temperature(unit='celsius')['temp'])
        temps.append(w.get_temperature(unit='celsius')['temp_max'])
        temps.append(w.get_temperature(unit='celsius')['temp_min'])
        status_arr.append(w.get_status())
        status_frequency[w.get_status()] = 0
        
    for s in status_arr:
        status_frequency[s] += 1

    result = "오늘의 날씨 - 최저 기온 {}'C / 최고 기온 {}'C {}".format( \
                                                                        min(temps), \
                                                                        max(temps), \
                                                                        max(status_frequency.items(), key=operator.itemgetter(1))[0])

    
    f = open('/tmp/weather_report', 'w')
    f.write(result)
    f.close()
        

@sched.scheduled_job('cron', hour=7, minute=0)
def notify_to_general_weather_summary():
    weather_report = get_weather_summary()
    slack_client = getattr(bot, '_client', None)
    channel_id = slack_client.find_channel_by_name(u'_잡담')
    slack_client.send_message(channel_id, weather_report)
