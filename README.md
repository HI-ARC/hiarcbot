# HI-ARC Bot

HI-ARC 슬랙에 상주하는 전자 생명체(?)입니다

## 개발 환경
* 언어 : Python 3.6
* 의존성관리 : [Pipenv](https://github.com/pypa/pipenv)
* 배포 : Docker, Docker-compose

## 실행하기

1. `cp docker-compose.yml.template docker-compose.yml` 명령을 실행한다.
2. Slack API Token을 얻어서 `SENSORED` 로 적어놓은 부분을 마저 채운다.
3. `docker pull <username>/hi-arc-bot:latest` 명령으로 도커 이미지를 끌고 오거나, 혹은 `docker build . -t <username>/hi-arc-bot:latest` 명령으로 도커 이미지를 빌드한다.
4. 빌드한 이미지를 이미 가지고 있다면, `docker-compose up` 명령을 커맨드라인에 입력해서 봇이 돌아가는 모습을 편-안하게 지켜보면 된다.

## 참고자료
* [slackbot](https://github.com/lins05/slackbot)