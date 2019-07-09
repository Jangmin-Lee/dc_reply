import re
import requests
import json
import re

from time import sleep

from bs4 import BeautifulSoup

url = 'http://gall.dcinside.com/board/lists/'
post_url = 'http://gall.dcinside.com/board/forms/comment_submit'

GALLERY_NAME = 'leagueoflegends2'
USER_NAME = '여폭찬'

payload = {'id': GALLERY_NAME, 'page': '1'}

HEADERS = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Host': 'gall.dcinside.com',
    'Upgrade-Insecure-Requests': '1',
}

post_HEADERS = {
    'Host': 'gall.dcinside.com',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Origin': 'http://gall.dcinside.com',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
}

data_name_list = [
    'id', 'no', 'cur_t', 'check_6', 'check_7', 'check_8', 'check_9', 'user_ip',
    'recommend', 't_vch2', 'service_code'
]

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

        print("\nurl은 " + article_url + " 입니다.\n")

        article_no = re.findall('\d\d+', article_url)

        session = requests.session()

        article_req = session.get(article_url, params=payload, headers=HEADERS)
        article_soup = BeautifulSoup(article_req.text, 'html.parser')

        div_reply_form = article_soup.find('div', 'view_comment')
        form_datas = div_reply_form.find_all('input')

        reply_data = dict()

        for form_data in form_datas:
            data_name = form_data.get('name', '')
            data_value = form_data.get('value', '')
            if data_name and data_value and data_name in data_name_list:
                reply_data[data_name] = data_value

        reply_data['ci_t'] = session.cookies['ci_c']
        reply_data['id'] = GALLERY_NAME
        reply_data['no'] = article_no[0]
        reply_data['t_vch2'] = None
        reply_data['name'] = 'ㅇㅇ'
        reply_data['password'] = 'asdasd'
        reply_data['memo'] = '댓글 주작기 테스트 중'

        print(json.dumps(reply_data, indent=4))

        post_req = requests.post(
            post_url, headers=post_HEADERS, data=reply_data)

        print("결과는 " + str(post_req) + " 입니다.")

        sleep(10)
