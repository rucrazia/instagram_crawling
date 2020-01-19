from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib.parse
from urllib.request import Request, urlopen
from time import sleep
import pandas as pd

search = input("검색어를 입력하세요 : ")
search = urllib.parse.quote(search)
url = 'https://www.instagram.com/explore/tags/' + str(search) + '/'
#driver = webdriver.Chrome('C:\\Users\\rucrazia\\Google 드라이브\\개발\\크롤링\\chromedriver')
driver = webdriver.Chrome('C:\\Users\\rucra\\Documents\\크롤링\\chromedriver')


driver.get(url)
sleep(5)

SCROLL_PAUSE_TIME = 1.0
reallink = []

main_iter = 0
while True:
    main_iter += 1
    pageString = driver.page_source
    bsObj = BeautifulSoup(pageString, "lxml")

    #bsObj = bsObj.find('h2', class_='yQ0j1', text='최근 사진')

    #print(bsObj.text)

    for link1 in bsObj.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):

        col_len = len(link1.find_all('a'))
        print(col_len)
        for i in range(col_len):
            title = link1.select('a')[i]
            real = title.attrs['href']
            reallink.append(real)
            print(title)
        break

    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    print(main_iter)
    if main_iter == 10:
        break

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
#reallinknum = len(reallink)

print("총" + str(reallinknum) + "개의 데이터.")

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
        #print(img_names)
        #for img in img_names:
            # img가 src 안에 있기 때문에 get_text가 아닌 src를 가져온다
            #print(img['src'])
        img_src = img.get("src")  # 이미지 경로
        #img_url = img_src  # 다운로드를 위해 base_url과 합침
        #img_name = str(i+1)+"번째 사진"  # 이미지 src에서 / 없애기
        #urllib.request.urlretrieve(img_url, "./img/" + img_name)



        print(str(i + 1) + "개의 데이터 받아오는 중.")
        print(csvtext)
        data = pd.DataFrame(csvtext)
        data.to_csv('insta.txt', encoding='utf-8')

except:
    print("오류발생" + str(i + 1) + "개의 데이터를 저장합니다.")

    data = pd.DataFrame(csvtext)
    data.to_csv('insta.txt', encoding='utf-8')


