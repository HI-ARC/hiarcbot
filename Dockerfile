FROM python:3.7

MAINTAINER rijgndqw012@gmail.com

COPY . /hi-arc-bot
WORKDIR /hi-arc-bot

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "bot.py"]
