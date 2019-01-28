import requests
from slackbot.bot import listen_to

from hiarcbot import bot, sched

url = "https://www.acmicpc.net/problem/"

@listen_to('백준 ([0-9]+)번 문제')
@listen_to('BOJ([0-9]+)')
def show_boj_problem(message, number):
    msg = "BOJ {}번 문제 : {}".format(str(number), url + str(number))
    message.send(msg)