from model import db, User
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from main import send_massage
from weather import get_weather


def get_user_by_channel(channel):
    user = User.query.filter_by(channel=str(channel)).first()
    return user


def get_step(channel):
    user = get_user_by_channel(channel)
    return user.step


def add_step(channel):
    user = get_user_by_channel(channel)
    user.step += 1
    db.session.commit()


def reflash_step(channel):
    user = get_user_by_channel(channel)
    user.step = -1
    db.session.commit()


def get_talk_subject(channel):
    user = get_user_by_channel(channel)
    return user.talk_subject


def set_talk_subject(channel, status):
    user = get_user_by_channel(channel)
    user.talk_subject = status
    db.session.commit()


def change_set_new_alarm(channel):
    user = get_user_by_channel(channel)
    user.set_new_alarm = not user.set_new_alarm
    db.session.commit()


def get_set_new_alarm(channel):
    user = get_user_by_channel(channel)
    return user.set_new_alarm

## 여기
# def set_alarm_time(channel, alarm_time):
#     user = get_user_by_channel(channel)
#     tmp = alarm_time.split()
#     hour = int(tmp[0][:-1])
#     minute = int(tmp[1][:-1])
#     time = hour * 100 + minute
#     user.alarm_time = time
#     db.session.commit()


def alarm_message(channel):
    user = get_user_by_channel(channel)
    msg = get_weather(user.location)
    if user.message != 'no message':
        msg += '\n'
        msg += user.message
    send_massage(channel, msg)
    user.message = 'no message'
    user.set_new_alarm = False
    db.session.commit()


def set_alarm_time_target(channel, alarm_time):
    user = get_user_by_channel(channel)
    tmp = alarm_time.split()
    hour = int(tmp[0][:-1])
    minute = int(tmp[1][:-1])
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    scheduler.add_job(alarm_message, 'cron', args=[channel], hour=hour, minute=minute)
    scheduler.start()
    time = hour * 100 + minute
    user.alarm_time = time
    db.session.commit()


def set_alarm_time(channel, alarm_time):
    t = threading.Thread(target=set_alarm_time_target, args=(channel, alarm_time))
    t.daemon = True
    t.start()
    change_set_new_alarm(channel)


def set_message(channel, message):
    user = get_user_by_channel(channel)
    user.message = message
    db.session.commit()


def set_location(channel, location):
    user = get_user_by_channel(channel)
    user.location = location
    db.session.commit()


def get_location(channel):
    user = get_user_by_channel(channel)
    return user.location