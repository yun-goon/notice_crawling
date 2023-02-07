from bs4 import BeautifulSoup
from datetime import date
import requests
import time
import telegram

# Fixed values
TOKEN = '텔레그램에서 발급받은 토큰'
CHAT_ID = '메세지를 전송할 채팅방 ID'
url = "https://teaching.korea.ac.kr/teaching/community/notice1.do"

# Telegram bot
# bot = telegram.Bot(token=TOKEN)

# requests, bs4
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")


# 클래스 구분이 명확하지 않은 페이지에서 공지사항 리스트(ul) 추출(사이트 구조 변경 시 수정 필요)
to_find_notice = soup.findAll("ul", attrs={"class": "m"})
grabed_notice = to_find_notice[1]

#print(to_find_notice)
#print(grabed_notice)

# 각 공지사항의 element에 접근하기 위해 공지사항 li elements를 리스트 자료구조로 변환
notice_list = grabed_notice.findAll('li')
#print(notice_list)

#오늘 날짜를 문자열로
today = date.today().isoformat().replace('-', '.')
print(type(today))

# 공지사항 전송
for notice in notice_list:
    post_date = notice.span.get_text().replace('교직팀', '')
    #print(notice)
    if(today == post_date): #오늘 게시글이 있으면
        title = notice.a.get_text()
        link = 'https://teaching.korea.ac.kr/teaching/community/notice1.do' + \
            notice.a['href']
        feed = '{0}\n\n게시일: {1}\n\n링크: {2}'.format(title, post_date, link)
        #print(feed)
        #bot.send_message(text=feed, chat_id=CHAT_ID)
        time.sleep(2)
    else:
        continue