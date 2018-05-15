from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

import stores
import cities

driver = webdriver.Chrome("/Users/sml/chromedriver")
count_start = 0
count_end = 0


def initCrawler():
    # ----------These are headless options-----------------
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    # Change Headless User-Agent to general User-Agent.
    TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome("/Users/sml/chromedriver", chrome_options=options)

    # -------------------------------------------------------


def getCount(query):
    driver.get("http://map.daum.net")
    delay = 2  # seconds
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'q')))
    except TimeoutException:
        print("Loading took too much time!")
    finally:
        elem.clear()
        elem.send_keys(query)
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        _html = driver.page_source
        soup = BeautifulSoup(_html, "lxml")
        count = soup.find("em", id="info.search.place.cnt")
        if len(count.text) > 3:
            return True
        else:
            count = int(count.text)
            if count > 524:
                return True
            else:
                return False


def getMapAndCrawlFirstPage(query):
    driver.get("http://map.daum.net")
    delay = 2  # seconds
    global count_start
    global count_end
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'q')))
    except TimeoutException:
        print("Loading took too much time!")
    finally:
        elem.clear()
        elem.send_keys(query)
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        _html = driver.page_source
        soup = BeautifulSoup(_html, "lxml")
        count = soup.find("em", id="info.search.place.cnt")
        count = int(count.text)
        for e in soup.find_all("li", class_="PlaceItem"):
            tempClass = stores.storeInfoClass()
            tempName = e.h6.a["title"]
            realName = tempName.split(" ")
            if realName[0] == query:
                tempClass.setName(realName[0])
                tempClass.setBranch(realName[1])
                stores.storeInfos.append(tempClass)
                count_end += 1
            else:
                continue
        for i in range(count_start, count_end):
            tempPhoneNums = []
            for e in soup.find_all("span", class_="phone"):
                tempPhoneNums.append(e.text)
            stores.storeInfos[i].setPhoneNum(tempPhoneNums[i])
        for i in range(count_start, count_end):
            tempAddresses = []
            for e in soup.find_all("span", class_="subAddress"):
                tempAddresses.append(e.text)
            stores.storeInfos[i].setAddress(tempAddresses[i])
        count_start = count_end
        try:
            clickElem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.ID, "info.search.place.more")))
            clickElem.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")
        finally:
            return count


def startCrawling(query, pageCount):
    # ******1페이지에 15개의 정보!******
    pageNo = 1
    global count_start
    global count_end
    _html = driver.page_source
    soup = BeautifulSoup(_html, "lxml")

    for e in soup.find_all("li", class_="PlaceItem"):
        tempClass = stores.storeInfoClass()
        tempName = e.h6.a["title"]
        realName = tempName.split(" ")
        if realName[0] == query:
            tempClass.setName(realName[0])
            tempClass.setBranch(realName[1])
            stores.storeInfos.append(tempClass)
            count_end += 1
        else:
            continue
    for i in range(count_start, count_end):
        tempPhoneNums = []
        for e in soup.find_all("span", class_="phone"):
            tempPhoneNums.append(e.text)
        stores.storeInfos[i].setPhoneNum(tempPhoneNums[i])
    for i in range(count_start, count_end):
        tempAddresses = []
        for e in soup.find_all("span", class_="subAddress"):
            tempAddresses.append(e.text)
        stores.storeInfos[i].setAddress(tempAddresses[i])
    count_start = count_end

    '''
      page = soup.find("a", id="info.search.page.no2")
      while page.text != None:
    '''

def printAllStores():
    for e in stores.storeInfos:
        print(e.getName() + "***" + e.getBranch() + "***" + e.getPhoneNum() + "***" + e.getAddress())


def main():

    query = input("상호명을 입력하세요: ")
    if getCount(query) == True:  # 525개 이상의 데이터
        print("A lot of datas!")
    else:  # 525개 미만의 데이터
        pageCount = getMapAndCrawlFirstPage(query)
        startCrawling(query, pageCount)
        printAllStores()

if __name__ == "__main__":
    main()


