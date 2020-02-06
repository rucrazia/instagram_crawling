from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib.parse
from urllib.request import Request, urlopen, urlretrieve
from time import sleep
import pandas as pd
import json

search = input("검색어를 입력하세요 : ")
keyword = search
search = urllib.parse.quote(search)
url = 'https://www.instagram.com/explore/tags/' + str(search) + '/'
# driver = webdriver.Chrome('C:\\Users\\rucrazia\\Google 드라이브\\개발\\크롤링\\chromedriver')
driver = webdriver.Chrome('C:\\Users\\user\\Documents\\project\\Crawling\\chromedriver')

driver.get(url)
sleep(5)

SCROLL_PAUSE_TIME = 1.0
reallink = []
reallink_img_recog = []
main_iter = 0

while True:
    main_iter += 1
    pageString = driver.page_source
    bsObj = BeautifulSoup(pageString, "lxml")

    for link1 in bsObj.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):

        col_len = len(link1.find_all('a'))
        for i in range(col_len):
            title = link1.select('a')[i]
            real = title.attrs['href']

            if real not in reallink:
                try:
                    img_recog = title.find('img', alt=True)['alt']
                    reallink.append(real)
                    reallink_img_recog.append(img_recog)
                except:
                    pass

    print(reallink)

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

data = pd.DataFrame(reallink)
data.to_csv('instat.csv', encoding='utf-8')
reallink = ['/p/B7p2RI4A-8t/']
reallinknum = len(reallink)

print("총" + str(reallinknum) + "개의 데이터.")
reallinknum = 0

try:
    for i in range(0, reallinknum):
        csvtext.append([])
        req = Request('https://www.instagram.com/p' + reallink[i], headers={'User-Agent': 'Mozilla/5.0'})
        # req = Request('https://www.instagram.com/p/p/B7gFuNrBEvA/', headers={'User-Agent': 'Mozilla/5.0'})

        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "lxml", from_encoding='utf-8')
        soup1 = soup.find("meta", attrs={"property": "og:description"})
        print(soup)
        reallink1 = soup1['content']
        reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
        reallink1 = reallink1[:20]
        if reallink1 == '':
            reallink1 = 'Null'
        csvtext[i].append(reallink1)

        # getTitle
        for reallink2 in soup.find_all("meta", attrs={"property": "og:title"}):
            reallink2 = reallink2['content']
            csvtext[i].append(reallink2)
            print("title = " + reallink2)

        # getUploadDate
        for reallink3 in soup.find_all("script", type='application/ld+json'):
            data = json.loads(reallink3.text)
            print(data["uploadDate"])

        # https://stackoverflow.com/questions/26192727/extract-content-of-script-with-beautifulsoup
        # getHashTag
        for reallink2 in soup.find_all("meta", attrs={"property": "instapp:hashtags"}):
            reallink2 = reallink2['content']
            csvtext[i].append(reallink2)

        # getImage
        for reallink2 in soup.find_all("meta", attrs={"property": "og:image"}):
            reallink2 = reallink2['content'].replace("amp;", "")
            csvtext[i].append(reallink2)

            urllib.request.urlretrieve(reallink2, "../image/" + keyword + str(i) + ".jpg")

        print(str(i + 1) + "개의 데이터 받아오는 중.")
        print(csvtext)
        data = pd.DataFrame(csvtext)
        data.to_csv('insta.csv', encoding='utf-8')

except:
    print("오류발생" + str(i + 1) + "개의 데이터를 저장합니다.")

    data = pd.DataFrame(csvtext)
    data.to_csv('insta.csv', encoding='utf-8')


