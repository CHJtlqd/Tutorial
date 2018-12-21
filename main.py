# -*- coding: utf-8 -*-
import json
import os
import re
from slacker import Slacker
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
slack = Slacker('xoxb-504131970294-508554322023-se0uipgMqrYq6rGjwFs8Pa8C')
# BOT_NAME='CHJ-MovieBot'
app = Flask(__name__)

slack_token = 'xoxb-504131970294-508554322023-se0uipgMqrYq6rGjwFs8Pa8C'
slack_client_id = '504131970294.506896754497'
slack_client_secret = '7237e729f985f18a1ee5d2dd8a255185'
slack_verification = 'Z5PZGra13NyA3Gi7z6Wmz8BQ'
sc = SlackClient(slack_token)
#영화 순위 표시
def _crawl_movie_rank():
    url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn'
    req = urllib.request.Request(url)
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
    keywords=[]
    for i, keyword in enumerate(soup.find_all('div',class_='tit3')):
        if i<10:
            keywords.append(str(i+1)+'위 '+keyword.get_text().strip())
    return u'\n'.join(keywords)

# 영화상세 페이지 찾기
def _crawl_movie_detail(title):
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    url = 'https://movie.naver.com'
    driver.get(url)

    driver.find_element_by_id('ipt_tx_srch').send_keys(title)
    driver.find_element_by_xpath("""//*[@class="srch_field_on _view"]/button""").click()
    current_url = driver.current_url
    req = urllib.request.Request(current_url)
    sourcecode = urllib.request.urlopen(current_url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
    t = soup.find('ul', class_='search_list_1')
    movie_detail = t.find('a')['href']
    return url+movie_detail

#영화 상세페이지 에서 리뷰 (+점수)
def _crawl_movie_reple(title):
    url=_crawl_movie_detail(title)
    req = urllib.request.Request(url)
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    reples=[]
    nums=[]
    keywords=[]
    for i, keyword in enumerate(soup.find_all('div', class_='score_result')):
        for j in keyword.find_all('div', class_='star_score'):
            d = (j.get_text().strip())
            nums.append(d)
        for j in keyword.find_all('div', class_='score_reple'):
            reple = j.find('p')
            reple = (reple.get_text().strip())
            reples.append(reple)
    #영화제목 먼저 띄우고 댓글이랑 점수 표시
    for i in range(len(nums)):
        keywords.append('\n'+reples[i]+'\t'+nums[i]+'점')
    return u'\n'.join(keywords)

#영화 줄거리
def _crawl_movie_summary(title):
    url = _crawl_movie_detail(title)
    req = urllib.request.Request(url)
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    return soup.find('p',class_='con_tx').get_text()


# 현재 상영작 크롤링
def _crawl_naver_now_movie():
    url = 'https://movie.naver.com/movie/running/current.nhn'
    req = urllib.request.Request(url)

    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    keywords = []
    # 영화 제목
    titles = []
    # 영화 관람가
    ratings = []
    # 영화 카테고리
    categorys = []
    # 영화 평점
    nums = []
    for i, keyword in enumerate(soup.find_all("dl", class_='lst_dsc')):
        # print(keyword)
        if i < 10:
            # 영화제목
            title = keyword.find('dt', class_='tit')
            titles.append(title.find("a").get_text())
            # 관람연령 파싱
            new_rating = (str(title.select("span")))
            new_rating = new_rating.split('>')[1].split('<')[0]
            # print(new_rating)
            ratings.append(new_rating)

            # 평점 파싱
            nums.append(keyword.find('span', class_='num').get_text())
            # 카테고리 파싱
            tag = keyword.find('span', class_='link_txt')
            category_list = []
            for category in tag.get_text().split(','):
                # print(category.strip())
                category_list.append(category.strip())
                # print(category_tuple)
            categorys.append(category_list)

    # print(titles)
    # print(categorys)
    # print(ratings)
    # print(nums)
    for i in range(len(ratings)):
        keywords.append(
            '영화제목: ' + titles[i] + '\n관람연령: ' + ratings[i] + '\n평점: ' + nums[i] + '\n카테고리: ' + str(categorys[i]) + '\n')
    return u'\n'.join(keywords)


# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    # print(text)
    url = 'https://movie.naver.com/movie/running/current.nhn'
    req = urllib.request.Request(url)

    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    keywords = []
    # 영화 제목
    titles = []
    # 영화 관람가
    ratings = []
    # 영화 카테고리
    categorys = []
    # 영화 평점
    nums = []
    for i, keyword in enumerate(soup.find_all("dl", class_='list_dsc')):
        if i < 10:
            # 영화제목
            title=keyword.find('dt',class_='tit')
            titles.append(title.find("a").get_text())

            #관람연령 파싱
            new_rating = (str(title.select("span")))
            new_rating = new_rating.split('>')[1].split('<')[0]
            # print(new_rating)
            ratings.append(new_rating)

            #평점 파싱
            nums.append(keyword.find('span',class_='num').get_text)
            #카테고리 파싱
            tag=keyword.find('span',class_='link_txt')
            category_tuple=()
            for category in tag.get_text().split(','):
                category_tuple+tuple(category.strip())
            categorys.append(category_tuple)


    for i in range(len(ratings)):
        keywords.append('영화제목: '+titles[i] + '\n관람연령: ' + ratings[i]+'\n평점: '+nums[i]+'\n카테고리: '+categorys[i]+'\n')

    # 한글 지원을 위해 앞에 unicode u를 붙힙니다. 
    return u'\n'.join(keywords)


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]
        if "안녕" in text:
            slack.chat.post_message(channel, "메뉴를 선택해주세요")
            slack.chat.post_message(channel, "1. 상영영화")
            slack.chat.post_message(channel, "2. 영화순위")
            slack.chat.post_message(channel, "3. 영화평점")
            slack.chat.post_message(channel, "4. 영화줄거리")


        keywords = _crawl_naver_now_movie(text)

        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
