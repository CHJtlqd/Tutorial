import json
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
from selenium import webdriver
import time

app = Flask(__name__)

slack_token = 'xoxb-504131970294-508554322023-se0uipgMqrYq6rGjwFs8Pa8C'
slack_client_id = '504131970294.506896754497'
slack_client_secret = '7237e729f985f18a1ee5d2dd8a255185'
slack_verification = 'Z5PZGra13NyA3Gi7z6Wmz8BQ'
sc = SlackClient(slack_token)

# def Remove_space(text):
#     text=text.replace(" ","")
#     return text
# def main():
#     print("영화 리뷰")
#
#     # 리뷰를 수집할 사이트 주소 입력
#     url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn"
#
#     # URL 주소에 있는 HTML 코드를 soup에 저장합니다.
#     soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
#
#     #영화 랭킹에 있는 순위 별 영화 링크
#     temp=list()
#     link=list()
#     movie_name=list()
#     for count,temp in enumerate(soup.find_all("div",class_="tit3")):
#         link.append("http://movie.naver.com"+temp.find("a")["href"])
#         movie_name.append(temp.find("a")["title"])
#         count+=1
#
#     print("순위   제목      링크")
#     for i in range(0,count) :
#         print(str(i+1)+movie_name[i].center(50)+"\n"+link[i].ljust(100)+"\n")

    #영화 검색
    # text = "삼 국"
    # search=False
    # for i in range(0,count+1) :
    #     if search is False and i is count :
    #         print(" ' " + text + " ' " + " 검색 실패\n")
    #     elif i is not count and Remove_space(text) in Remove_space(movie_name[i].strip()):
    #         print(" ' " + text+" ' "+"을 검색 합니다.\n->"+movie_name[i])
    #         search=True





    #셀레니움 이용한 영화관
def search_theater(search):
    search_text=search
    keyword=list()
    keyword.append(search_text)
    keyword.append(" 영화관")
    next_button = webdriver.Chrome()

    next_button.get("https://search.naver.com")
    next_button.find_element_by_name("query").send_keys(keyword)

    next_button.find_element_by_xpath("//span[@class='ico_search_submit']").click()

    # URL 주소에 있는 HTML 코드를 soup에 저장합니다.
    soup = BeautifulSoup(urllib.request.urlopen(next_button.current_url).read(), "html.parser")
    keywords=list()
    theater=list()
    theater_list = soup.find("div", class_="_wrap_theater_list")
    kk = theater_list.find("tbody", class_="_theater_list")
    for i in kk.find_all('span',class_='map_pst'):
        temp=i.get_text().split('\n')
        temp=temp[0][1:]
        theater.append(temp)
    for num,i in enumerate(kk.find_all("span", class_="els")):
        keywords.append(theater[num]+'\t'+ i.get_text())
    print(keywords)
    #print(theater)

search_theater('구미')
#next_button.implicitly_wait(60)

#time.sleep(10)
#
# if __name__ == "__main__":
#     main()