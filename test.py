import requests
import time
import telegram
from bs4 import BeautifulSoup
from datetime import date
import logging
import pandas
import lxml
import asyncio
import schedule

headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "sec-ch-ua-mobile": "?0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9"
}

# Fixed values
TOKEN = '6023105153:AAFu0pruC11fYbC-b-ZQQ_gMgVjrExG4oH8'
CHAT_ID = '-1001877056305'
url = 'https://www.kw.ac.kr/ko/life/notice.jsp?srCategoryId=&mode=list&searchKey=1&searchVal='

# Telegram bot
bot = telegram.Bot(token=TOKEN)


def main():
    # requests, bs4
    res = requests.get(url, headers=headers)
    res.raise_for_status() #에러가 났으면 멈추고, 에러를 알려줌
    soup = BeautifulSoup(res.text, "lxml") 

    # 공지사항 목록 받기
    to_find_notice = soup.find_all("li", {'class' : 'top-notice'})
    #오늘 날짜를 문자열로
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))
        # 공지사항 전송
    for notice in to_find_notice:
        post_date = notice.p.get_text().split()[4] #7 : 수정일 4 : 게시일
        if(today == post_date or post_date == yesterday): #오늘, 어제 게시글이 있으면
            title = notice.a.get_text().split('\n')[1]
            link = 'https://www.kw.ac.kr' + \
                notice.a['href']
            feed = '{0}\n\n게시일: {1}\n\n링크: {2}'.format(title, post_date, link)
            logging(feed,"\n")
            bot.send_message(text=feed, chat_id=CHAT_ID)
            time.sleep(2)
        else:
            continue

#schedule.every(1).day.at("9:00").do(main) #매일 9시에 실행
schedule.every(1).minutes.do(main) #매 1분마다 실행

while True:
    schedule.run_pending()
    time.sleep(1)

#loop = asyncio.get_event_loop()
#loop.run_until_complete(main())
#loop.close()