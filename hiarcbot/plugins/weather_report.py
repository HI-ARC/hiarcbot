import re
import requests

from slackbot.bot import respond_to

from hiarcbot import bot, sched
import slack_config

url = 'https://api2.sktelecom.com/weather/summary'
params = {
    'version': 1,
    'stnid': 108,  # 여의도 관측소
}
headers = {
    'appKey': slack_config.WEATHER_PLANET_API_KEY,
}


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


def basic_response():
    return '[{day}의 날씨]\n({status} / 최저 온도 : {t_min}도 , 최고 온도 : {t_max}도)\n'


def get_weather_summary():
    r = requests.get(url=url, params=params, headers=headers)
    if r.status_code != 200:
        body = r.json().get('error')
        code = body.get('code', '?')
        msg = body.get.get('message', '아무튼 실패함')
        return 'error code {}: {}'.format(code, msg)

    summary = r.json()['weather']['summary'][0]
    columns = {'today': '오늘', 'tomorrow': '내일', 'dayAfterTomorrow': '모레'}

    def extract_message(day):
        day_name = columns.get(day)
        status = sky_code_to_message_with_emoji(summary[day]['sky']['code'])
        temperature_min = summary[day]['temperature']['tmin']
        temperature_max = summary[day]['temperature']['tmax']

        msg = basic_response().format(
            day=day_name,
            status=status,
            t_min=temperature_min,
            t_max=temperature_max)
        return msg

    weather_report = '\n'.join(map(extract_message, columns))
    return weather_report


@respond_to('^날씨$', re.IGNORECASE)
def help(message):
    weather_report = get_weather_summary()
    message.send(weather_report)


@sched.scheduled_job('cron', hour=7, minute=0)
def notify_to_general_weather_summary():
    weather_report = get_weather_summary()
    slack_client = getattr(bot, '_client', None)
    channel_id = slack_client.find_channel_by_name(u'_잡담')
    slack_client.send_message(channel_id, weather_report)
