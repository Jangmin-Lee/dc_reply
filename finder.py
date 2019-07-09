import re
import requests
import json
import re

import smtplib
from email.mime.text import MIMEText

from bs4 import BeautifulSoup

url = 'http://gall.dcinside.com/board/lists/'
post_url = 'http://gall.dcinside.com/board/forms/comment_submit'

# 원하는 갤러리 아이디 (주소창에 위치)
GALLERY_NAME = 'leagueoflegends2'
# 원하는 갤러 닉
USER_NAME = ''

payload = {'id': GALLERY_NAME, 'page': '1'}

HEADERS = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Host': 'gall.dcinside.com',
    'Upgrade-Insecure-Requests': '1',
}

req = requests.get(url, params=payload, headers=HEADERS)

soup = BeautifulSoup(req.text, 'html.parser')
div_list = soup.find('div', 'gall_listwrap list')
div_articles = div_list.find_all('tr')

for div_article in div_articles:
    article_user = div_article.find('td', 'gall_writer ub-writer')

    if not article_user:
        continue

    user_name = article_user.get_text()

    if re.search(USER_NAME, user_name):
        td_article_part = div_article.find('td', 'gall_tit ub-word')
        a_tag_url = td_article_part.find('a')['href']

        article_url = 'http://gall.dcinside.com' + a_tag_url

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()      # say Hello
        smtp.starttls()  # TLS 사용시 필요
        # https://medium.com/@mika94322/python-smtp-email-%EC%A0%84%EC%86%A1-%EC%98%88%EC%A0%9C-c7e6e095dcfc 참고하여 비밀번호
        # 구글 아이디와 비밀번호
        smtp.login('구글이메일', '구글앱 비밀번호')

        msg = MIMEText("글 주소는 " + article_url)
        msg['Subject'] = '새로운 글 알림'
        msg['To'] = '받는 이메일 주소'
        smtp.sendmail('구글이메일', '받는 이메일 주소', msg.as_string())

        smtp.quit()
