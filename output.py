from main import send_massage
from const import *

init_msg = "안녕하세요~\n" \
           "저는 출근시간 당담 '출리미' 입니다!\n" \
           "내일 아침에 받고싶은 알람 메세지를 저에게 설정해주세요!\n" \
           "원하는 시간에 내일 날씨 정보와 함께 보내드립니다!!\n" \
           "이제 사용법을 알려드리겠습니다!\n"\
           "'지역설정'을 입력하시면 날씨 정보를 받을 지역을 설정하고 '시간설정'을 입력하면 알람 받을 시간을 설정합니다\n" \
           "그리고 '메시지'를 입력하면 알람 받을 메세지를 설정합니다!!\n"


def init_message(channel):
    send_massage(
        channel,
        init_msg
    )


def talk_conversation(status, channel):
    if status == TalkSubject.TIME:
        send_massage(
            channel,
            "'0시 00분'으로 입력해주세요! 형식을 꼭 맞춰주세요!(예: 7시 45분, 14시 41분)"
        )

    elif status == TalkSubject.MESSAGE:
        send_massage(
            channel,
            "알림받을 메시지를 자유롭게 입력해주세요!"
        )
    elif status == TalkSubject.LOCATION:
        send_massage(
            channel,
            "지역을 입력해주세요!(예: 서울)"
        )
