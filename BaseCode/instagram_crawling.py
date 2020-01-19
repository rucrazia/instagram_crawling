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
    #'C:\\Users\\rucra\\Documents\\크롤링\\chromedriver'

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


    def get_image_list(self, soup):
        driver.get(url)
        sleep(5)

        SCROLL_PAUSE_TIME = 1.0
        reallink = []

        while True:
            pageString = driver.page_source
            bsObj = BeautifulSoup(pageString, "lxml")

            #date_field.find_next_sibling('dd').text.strip()
            for link1 in bsObj.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):

                col_len = len(link1.find_all('a'))
                print(col_len)
                for i in range(col_len):
                    title = link1.select('a')[i]
                    real = title.attrs['href']
                    reallink.append(real) #사진들 link 가져오기
                    print(title)

            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)
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

        csvtext = []

        reallinknum = len(reallink)
        # reallinknum = len(reallink)

        print("총" + str(reallinknum) + "개의 데이터.")

        return reallink

    def get_keywords(self, soup):

        try:
            for i in range(0, reallinknum):

                csvtext.append([])
                req = Request('https://www.instagram.com/p' + reallink[i], headers={'User-Agent': 'Mozilla/5.0'})

                webpage = urlopen(req).read()
                soup = BeautifulSoup(webpage, "lxml", from_encoding='utf-8')
                soup1 = soup.find("meta", attrs={"property": "og:description"})

                reallink1 = soup1['content']
                reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
                reallink1 = reallink1[:20]
                if reallink1 == '':
                    reallink1 = 'Null'
                csvtext[i].append(reallink1)

                for reallink2 in soup.find_all("meta", attrs={"property": "instapp:hashtags"}):
                    reallink2 = reallink2['content']
                    csvtext[i].append(reallink2)

                img_names = soup.find_all("img")  # 이미지 태그
                print(img_names)
                for img in img_names:
                    ## img가 src 안에 있기 때문에 get_text가 아닌 src를 가져온다
                    print(img['src'])
                img_src = img.get("src")  # 이미지 경로
                # img_url = img_src  # 다운로드를 위해 base_url과 합침
                # img_name = str(i+1)+"번째 사진"  # 이미지 src에서 / 없애기
                # urllib.request.urlretrieve(img_url, "./img/" + img_name)

                print(str(i + 1) + "개의 데이터 받아오는 중.")
                print(csvtext)
                data = pd.DataFrame(csvtext)
                data.to_csv('insta.txt', encoding='utf-8')

        except:
            print("오류발생" + str(i + 1) + "개의 데이터를 저장합니다.")

            data = pd.DataFrame(csvtext)
            data.to_csv('insta.txt', encoding='utf-8')

        return keywords_list

    def get_uploadTime(self):
        pass

    def get_text(self):
        pass

    def get_date(self):
        pass



    def make_csvFile(self, data):
        csvfile = open("C://Users//rucrazia//Documents//Downloads//test.csv", "w", newline="")
        csvwriter = csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)
        csvfile.close()

