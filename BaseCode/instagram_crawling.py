# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 21:44:29 2020

@author: rucrazia

ref:
    https://jh-0323.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%9C%A0%ED%8A%9C%EB%B8%8C-%EC%B1%84%EB%84%90-%ED%81%AC%EB%A1%A4%EB%A7%81-csv%ED%8C%8C%EC%9D%BC%EB%A1%9C-%EB%A7%8C%EB%93%A4%EA%B8%B0
    https://yeowool0217.tistory.com/552
"""

import requests
from bs4 import BeautifulSoup
import time
import urllib.request #
from selenium.webdriver import Chrome
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime as dt
from selenium import webdriver
from time import localtime, strftime
import csv

from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib.parse
from time import sleep
import pandas as pd
from multiprocessing import Pool, Value, freeze_support


class InstagramCrawler:

    def __init__(self):
        pass
    #'C:\\Users\\rucrazia\\Google 드라이브\\개발\\크롤링\\chromedriver'


    def setting(self, driverRoot):
        mobile_emulation = {"deviceName": "Nexus 5"}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        # https://www.youtube.com/?persist_app=1&app=desktop
        driver = webdriver.Chrome(driverRoot,
                                  desired_capabilities=chrome_options.to_capabilities())
        return driver

    #'https://m.youtube.com/user/BuzzBean11/videos'
    def get_targetPage(self, driver, pageUrl):
        driver.get(pageUrl)

        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        time.sleep(3)

        return soup

    def get_youtuberInfo(self, soup):

        youtuberName = soup.find('h1', 'c4-tabbed-header-title').text

    num = 0

    def f(x):
        frame = []
        global num

        req = Request('https://www.instagram.com/p' + x, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "lxml", from_encoding='utf-8')
        soup1 = soup.find("meta", attrs={"property": "og:description"})
        reallink1 = soup1['content']
        reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
        reallink1 = reallink1[:20]
        if reallink1 == '':
            return
        # mylist.append(reallink1)

        for reallink2 in soup.find_all("meta", attrs={"property": "instapp:hashtags"}):
            reallink2 = reallink2['content']
            reallink2 = reallink2[:10]
            mylist = []

            mylist.append(reallink1)
            mylist.append(reallink2)

            frame.append(mylist)

        print(str(num) + "개의 데이터 저장 중")
        num += 1
        data = pd.DataFrame(frame)
        data.to_csv('insta.txt', mode='w', encoding='utf-8', header=None)


    def get_youtuberVideo(self, soup):

        freeze_support()

        print('### jinho021712@gmail.com ### Instacrawler Ver 0.1')

        print("pass")
        print("#크롤링 속도는 컴퓨터 사양에 따라 1.0 ~ 2.5 값으로 설정해주세요.")

        scrolltime = float(input("크롤링 속도를 입력하세요 : "))
        crawlnum = int(input("가져올 데이터의 수를 입력하세요 : "))
        search = input("검색어를 입력하세요 : ")
        search = urllib.parse.quote(search)
        url = 'https://www.instagram.com/explore/tags/' + str(search) + '/'
        driver = webdriver.Chrome('chromedriver.exe')

        driver.get(url)
        sleep(5)

        SCROLL_PAUSE_TIME = scrolltime
        reallink = []

        while True:
            pageString = driver.page_source
            bsObj = BeautifulSoup(pageString, "lxml")

            for link1 in bsObj.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):
                title = link1.select('a')[0]
                real = title.attrs['href']
                reallink.append(real)
                title = link1.select('a')[1]
                real = title.attrs['href']
                reallink.append(real)
                title = link1.select('a')[2]
                real = title.attrs['href']
                reallink.append(real)

            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME) #Scroll
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break

                else:
                    last_height = new_height
                    continue

        reallinknum = len(reallink)
        print("총" + str(reallinknum) + "개의 데이터를 받아왔습니다.")

        p = Pool(5)
        p.map(f, reallink)
        p.close()
        p.join()
        print("저장완료")




        return youtube_video_list


    def make_csvFile(self, data):
        csvfile = open("C://Users//rucrazia//Documents//Downloads//test.csv", "w", newline="")
        csvwriter = csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)
        csvfile.close()

