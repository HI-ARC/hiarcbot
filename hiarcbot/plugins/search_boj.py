import re
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup as Soup
from slackbot.bot import respond_to

from hiarcbot import bot, sched

url = "https://www.acmicpc.net/search#"

'''
def search_boj_problem(pattern):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) '
                    'Chrome/52.0.2743.116 Safari/537.36'
    }

    query = { 'q': pattern, 'c': 'Problems' }
    query_string = urlencode(query_string, 'utf-8')
    full_url = url + query_string

    res = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        return '[System] 앗.... 에러가 발생했어요 ㅜㅜ'

    title_soup       = Soup(res.text, 'html.parser')
    description_soup = Soup(res.text, 'html.parser') 

    matched_title        = soup.select('#result > div.results > div.inner-results > h3 > a')
    matched_descriptions = soup.select('#result > div.results > div.inner-results > h3 > a')
    for result in matched_results:



@respond_to('^백준검색 ([가-힣a-zA-Z]+)$')
def search_boj(message, pattern):
    result = search_boj_problem(pattern)
    message.reply(result)



@respond_to('^ebook$', re.IGNORECASE)
def today_free_ebook(message):
    title = get_today_ebook_title()
    message.send("[ 오늘의 무료 EBook ]\n"
                 "%s\n%s" % (title, url))
'''