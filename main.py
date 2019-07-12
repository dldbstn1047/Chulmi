from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from time import sleep
from input import *
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dbstnWkd@127.0.0.1:3306/chulimi?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SLACK_TOKEN = 'xoxb-677120743489-689181830420-NAW0CLWVY1xG5EaPMs05l5t2'
SLACK_SIGNING_SECRET = '61b80d4cdd52adff6a928f0ea03028b9'

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)


scheduler = BackgroundScheduler(timezone='Asia/Seoul')


@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]
    text = text[13:]
    user = get_user_by_channel(channel)
    print(type(user))
    if user is None:
        user = User(channel=channel)
        db.session.add(user)
        db.session.commit()
    add_step(channel) # step 초기값을 -1이라고 하면, add하고 시작하니까 0으로 시작
    go_conversation(channel, text)


def send_massage(channel, message):
    slack_web_client.chat_postMessage(
        channel=channel,
        text=message
    )


def sleep_message():  # 오후 11시에 발동하는 함수
    users = User.query.filter_by(set_new_alarm=False).all()  # 새로 시간을 등록 안한 사람전부를 가져온다.
    for user in users:
        channel = user.channel
        msg = '아직 내일 알람이 설정되어있지 않습니다!\n' \
              '"시간"을 입력하여 알람 시간과 메시지를 설정해 주세요~'
        send_massage(channel, msg)


scheduler.add_job(sleep_message, 'cron', hour=23) #밤 11시 알림

if __name__ == '__main__':
    db.create_all()
    scheduler.start()
    db.init_app(app)

    #### 테스트용
    user = User.query.filter_by(channel='CKY743NSW').first()
    user.step = -1
    user.talk_subject = 0
    user.set_new_alarm = False
    user.location = 'no location'
    user.message = 'TEST 메세지'
    db.session.commit()
    ####

    app.run('0.0.0.0', port=5000)