import urllib.request
from bs4 import BeautifulSoup
import datetime

city = {'부천':'CT001012', '서울':'CT001013', '성남':'CT001014', '수원':'CT001015',
        '강릉':'CT004001', '속초':'CT004007', '부산':'CT008008'}


def get_weather(area):

    url = 'https://weather.naver.com/rgn/cityWetrCity.nhn?cityRgnCd='+city[area]
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    cur_info = soup.find('div', class_='fl').em.get_text(strip=True)
    temperature = cur_info[:cur_info.find('℃')+1]  # 온도
    forecast = cur_info[cur_info.find('℃')+1:]  # 날씨예보

    cur_info_detail = soup.find('div', class_='fl').p.get_text(strip=True)
    yesterday = cur_info_detail[:cur_info_detail.find('|')]     # 어제보다 어쩌고
    dust = cur_info_detail[cur_info_detail.find('%')+5:cur_info_detail.find('%')+7]     # 미세먼지 (좋음 보통 나쁨)

    utcnow = datetime.datetime.utcnow()
    time_gap = datetime.timedelta(hours=9)
    kor_time = utcnow + time_gap
    time_format = '%H시 %M분'.encode('unicode-escape').decode()
    kor_time_h_m = kor_time.strftime(time_format).encode().decode('unicode-escape')

    umbrella = '> 아직까진 비소식이 없나봐요~\n'
    if '비' in forecast or '소나기' in forecast:
        umbrella = '비가 올 수도 있으니 우산을 챙기세요~\n'

    mask = '> 오늘은 미세먼지가 좋아요!!!>_<\n'
    if dust == '나쁨':
        mask = '미세먼지가 나쁜 날이니 마스크를 꼭 챙기세요~\n'

    msg = '현재 시간은 '+kor_time_h_m+'\n'+area+'의 온도는 '+temperature+'\n'+yesterday+'입니다!\n'+umbrella+mask

    return msg