import re
from main import send_massage
from output import *
from alarm import *
from const import *


def go_conversation(channel, text):
    # 대화 맨 처음
    if get_step(channel) == 0:
        if '시간' in text:
            location = get_location(channel)
            if location == 'no location':
                send_massage(channel, "지역이 설정되어 있지 않습니다~ '지역'을 입력하여 지역을 먼저 설정 해주세요!!")
                reflash_step(channel)
            else:
                set_talk_subject(channel, TalkSubject.TIME)
                talk_conversation(TalkSubject.TIME, channel)
        elif '메시지' in text:
            is_alarm = get_set_new_alarm(channel)
            if is_alarm is False:
                send_massage(channel, "시간이 설정되어 있지 않습니다~ '시간'을 입력하여 시간을 먼저 설정 해주세요!!")
                reflash_step(channel)
            else:
                set_talk_subject(channel, TalkSubject.MESSAGE)
                talk_conversation(TalkSubject.MESSAGE, channel)
        elif '지역' in text:
            set_talk_subject(channel, TalkSubject.LOCATION)
            talk_conversation(TalkSubject.LOCATION, channel)
        else:  # 아무말 했으면 포맷 안내 메시지 output
            reflash_step(channel)
            init_message(channel)
    # 대화 중간
    else:
        # 알람 시간 설정 대화
        if get_talk_subject(channel) == TalkSubject.TIME:
            if re.compile("\d+시 \d+분").match(text) is not None:
                set_talk_subject(channel, 0)
                reflash_step(channel)
                send_massage(channel, "'" + text + "'로 설정되었습니다!")
                set_alarm_time(channel,text)
            else:   # 입력 포맷이 틀렸을 경우 다시 질문
                talk_conversation(TalkSubject.TIME, channel)

        # 메시지 설정 대화
        elif get_talk_subject(channel) == TalkSubject.MESSAGE:
            set_talk_subject(channel, 0)
            reflash_step(channel)
            set_message(channel, text)
            send_massage(channel, "'" + text + "'로 설정되었습니다!")

        # 지역 설정 대화
        elif get_talk_subject(channel) == TalkSubject.LOCATION:
            if text == '서울' or text == '부산' or text == '부천' or text == '속초':
                set_talk_subject(channel, 0)
                reflash_step(channel)
                set_location(channel, text)
                send_massage(channel, "'" + text + "'로 설정되었습니다!")
            else:
                talk_conversation(TalkSubject.LOCATION, channel)

