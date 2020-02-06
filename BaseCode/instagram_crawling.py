from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib.parse
from urllib.request import Request, urlopen, urlretrieve
from time import sleep
import pandas as pd
import json
import datetime
from urllib.parse import quote
from pathlib import Path


class InstagramCrawler():
    csvtext = []
    keyword = ''

    def get_origin_csv_id_list(self, origin_csv):
        origin_id_list = origin_csv.iloc[-12:]
        origin_id_list = origin_id_list['ID']
        print(origin_id_list.values.tolist())
        return origin_id_list

    def get_content_title(self, soup, iterate_count):
        title = ''
        for reallink2 in soup.find_all("meta", attrs={"property": "og:title"}):
            title = reallink2['content']
            if title is None:
                self.csvtext[iterate_count].append('non_title_R')
            else:
                self.csvtext[iterate_count].append(title)

    def get_content_upload_date(self, soup, iterate_count):
        # script = soup.find('script')
        # page_json = script.text.split(' = ', 1)[1].rstrip(';')
        # data = json.loads(page_json)
        # upload_date = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_tagged_user']['edges'][0]['node']['user']['id']
        # upload_date = datetime.datetime.fromtimestamp(timestamp/1000)
        # print(upload_date)

        upload_date = None
        for reallink3 in soup.find_all("script", type='application/ld+json'):
            data = json.loads(reallink3.text)
            upload_date = data["uploadDate"]

        if upload_date is None:
            self.csvtext[iterate_count].append('non_upload_date_R')
        else:
            self.csvtext[iterate_count].append(str(upload_date))

    def get_contents_image_jpg(self, soup, keyword, iterate_count):
        for reallink2 in soup.find_all("meta", attrs={"property": "og:image"}):
            reallink2 = reallink2['content'].replace("amp;", "")
            self.csvtext[iterate_count].append(reallink2)
            # urllib.request.urlretrieve(reallink2, "../image/"+keyword+str(iterate_count)+".jpg")
            urllib.request.urlretrieve(reallink2, "C:\\Users\\user\\Documents\\project\\크롤링\\image\\" + keyword + str(
                iterate_count) + ".jpg")

    '''
    def get_content_description(self, soup, iterate_count):   
        soup1 = soup.find("meta", attrs={"property": "og:description"})

        reallink1 = soup1['content']
        reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
        reallink1 = reallink1[:20]

        print(reallink1)
        if reallink1 == '':
            reallink1 = 'non_description_R'
        self.csvtext[iterate_count].append(reallink1)
    '''

    def get_content_hashtag(self, soup, iterate_count):

        hashtag_list = []
        '''
        script = soup.find('script', text=lambda t: \
                           t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        print(data['edge_media_to_tagged_user'])
        '''
        # add_comment_hashtag = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['aption_is_edited']['edges'][0]['node']['user']['id']

        # if add_comment_hashtag ==

        for reallink2 in soup.find_all("meta", attrs={"property": "instapp:hashtags"}):
            reallink2 = reallink2['content']
            hashtag_list.append(reallink2)

        if len(hashtag_list) == 0:
            self.csvtext[iterate_count].append(['None_Hashtag_R'])
        else:
            self.csvtext[iterate_count].append(hashtag_list)

    def get_images_data(self, driver, image_list, origin_csv):

        image_link_list = image_list[0]
        image_recog_list = image_list[1]
        image_link_len = len(image_link_list)
        # image_link_len = 4

        print("link " + str(image_link_list))
        print("link len = " + str(image_link_len))

        try:
            for i in range(0, image_link_len):
                self.csvtext.append([i])
                self.csvtext[i].append(image_link_list[i].replace("/p/", "").replace("/", ""))
                # 봇으로 인해 정지되었을 때 req에다 header를 넣어주어 user agent를 입력하면 봇으로 인식 못한다.
                ## https://m.blog.naver.com/PostView.nhn?blogId=kiddwannabe&logNo=221185808375&proxyReferer=https%3A%2F%2Fwww.google.com%2F
                #            req = Request('https://www.instagram.com/p' + image_link_list[i], headers={'User-Agent': 'Mozilla/5.0'})

                req = Request('https://www.instagram.com/p' + image_link_list[(i * 2)], headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'})

                # yourstring = yourstring.encode('ascii', 'ignore').decode('ascii')
                # req = Request('https://www.instagram.com/p/p/B7gFuNrBEvA/', headers={'User-Agent': 'Mozilla/5.0'})

                webpage = urlopen(req).read()

                soup = BeautifulSoup(webpage, "lxml", from_encoding='utf-8')

                self.csvtext[i].append(self.keyword)
                self.get_content_title(soup, i)
                self.get_content_upload_date(soup, i)
                self.get_content_hashtag(soup, i)
                self.csvtext[i].append(image_recog_list[i])
                self.get_contents_image_jpg(soup, self.keyword, i)

                # https://stackoverflow.com/questions/26192727/extract-content-of-script-with-beautifulsoup
                print(str(i + 1) + "개의 데이터 받아오는 중.")
                # print(self.csvtext)

                # print(self.csvtext)

        except:

            print("오류발생" + str(i + 1) + "번째")

            # data = pd.DataFrame(self.csvtext, columns=['NUM','ID','KEYWORD', 'TITLE', 'UPLOAD_DATE','DESCRIPTION','HASHTAG','IMAGE_URL'])
            # data.to_csv('insta.csv', encoding='utf-8', sep='\t', index=False)

        data_csv = pd.DataFrame(self.csvtext,
                                columns=['INDEX', 'ID', 'KEYWORD', 'TITLE', 'UPLOAD_DATE', 'HASHTAG', 'IMAGE_RECOG',
                                         'IMAGE_URL'])

        data = pd.concat([origin_csv, data_csv])

        data.to_csv('insta2.csv', encoding='utf-8', sep='\t', index=False)

    def get_images_list(self, driver, origin_id_list):

        SCROLL_PAUSE_TIME = 1.0
        image_list = []
        reallink = []
        reallink_img_recog = []
        main_iter = 0

        while True:
            main_iter += 1
            pageString = driver.page_source
            bsObj = BeautifulSoup(pageString, "lxml")
            origin_flag = False

            for link1 in bsObj.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):

                col_len = len(link1.find_all('a'))
                for i in range(col_len):
                    title = link1.select('a')[i]
                    real = title.attrs['href']

                    if real not in reallink:
                        if real not in origin_id_list:
                            try:  # 동영상이 나오게 되면 ERROR가 뜨게 되므로 try catch로 넘김
                                img_recog = title.find('img', alt=True)['alt']
                                reallink.append(real)
                                reallink_img_recog.append(img_recog)
                            except:
                                pass

            if origin_flag == True:
                print("return")
                break

            if main_iter == 4:
                break

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

        image_list = [reallink, reallink_img_recog]
        return image_list

    def init_get_driver(self, search):
        self.keyword = search
        search = urllib.parse.quote(search)
        url = 'https://www.instagram.com/explore/tags/' + str(search) + '/'
        # driver = webdriver.Chrome('C:\\Users\\rucrazia\\Google 드라이브\\개발\\크롤링\\chromedriver')
        driver = webdriver.Chrome('C:\\Users\\user\\Documents\\project\\Crawling\\chromedriver')

        driver.get(url)
        sleep(2)

        return driver

    def main(self, search):

        my_file = Path("insta.csv")
        if my_file.is_file():
            # file exists
            origin_csv = pd.read_csv('insta2.csv', encoding='utf-8', sep='\t')
        else:
            origin_csv = pd.DataFrame(
                columns=['INDEX', 'ID', 'KEYWORD', 'TITLE', 'UPLOAD_DATE', 'HASHTAG', 'IMAGE_RECOG',
                         'IMAGE_URL'])
        origin_id_list = self.get_origin_csv_id_list(origin_csv)

        driver = self.init_get_driver(search)
        image_list = self.get_images_list(driver, origin_id_list)
        self.get_images_data(driver, image_list, origin_csv)


if __name__ == "__main__":
    # execute only if run as a script
    search = input("검색어를 입력하세요 : ")

    instagam_crawler_class = InstagramCrawler()
    instagam_crawler_class.main(search)



