# virtualenv 생성
virtualenv -p python3 venv
source venv/bin/activate

# 의존 라이브러리 설치
pip install -r requirements.txt

python bot.py
