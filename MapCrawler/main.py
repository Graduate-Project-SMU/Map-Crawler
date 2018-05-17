from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import crawler_config
import stores as s
import cities as c



delay = 0
driver = None
count_start = 0
count_end = 0
store_infos = []


driver = webdriver.Chrome("/Users/sml/chromedriver")

'''
def init():
    global driver
    driver = crawler_config.initCrawler()
'''

def getCount(query):
    global driver
    global delay
    global store_infos
    driver.get("http://map.daum.net")
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
            totCount = int(count.text)
            if totCount > 524:
                return True
            else:
                return False

def crawlList(query):
    global count_start
    global count_end
    global store_infos
    _html = driver.page_source
    soup = BeautifulSoup(_html, "lxml")
    for e in soup.find_all("li", class_="PlaceItem"):
        tempClass = s.storeInfoClass()
        tempName = e.h6.a["title"]
        realName = tempName.split(" ")
        if realName[0] == query:
            tempClass.setName(realName[0])
            if len(realName) == 2:
                tempClass.setBranch(realName[1])
            else :
                tempClass.setBranch("")
            tempPhoneNum = e.find("span", class_="phone")
            tempClass.setPhoneNum(tempPhoneNum.text)
            tempAddress = e.find("span", class_="subAddress")
            if tempAddress != None:
                tempClass.setAddress(tempAddress.text)
            else :
                tempClass.setAddress("Unknown")
            store_infos.append(tempClass)
            count_end += 1
        else:
            continue
    count_start = count_end

def getMapAndCrawlFirstPageUnder525(query):
    global driver
    global delay
    global count_start
    global count_end
    global store_infos
    driver.get("http://map.daum.net")
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
        total_data_count = int(count.text)
        crawlList(query)
        try:
            clickElem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.ID, "info.search.place.more")))
            clickElem.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")
        finally:
            return total_data_count

def getMapAndCrawlFirstPage(query, locationQuery):
    global driver
    global delay
    global count_start
    global count_end
    global store_infos
    driver.get("http://map.daum.net")
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'q')))
    except TimeoutException:
        print("Loading took too much time!")
    finally:
        elem.clear()
        elem.send_keys(locationQuery)
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        _html = driver.page_source
        soup = BeautifulSoup(_html, "lxml")
        count = soup.find("em", id="info.search.place.cnt")
        total_data_count = int(count.text)
        crawlList(query)
        try:
            clickElem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.ID, "info.search.place.more")))
            clickElem.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")
        finally:
            return total_data_count

def startCrawling(query, totalDataCount):
    # ******1페이지에 15개의 정보!******
    global driver
    global count_start
    global count_end
    global delay
    global store_infos
    pagingString = "info.search.page.no"
    tempIntNum = int(totalDataCount/15)
    if totalDataCount % 15 != 0:
        totalPage = tempIntNum + 1
    else :
        totalPage = tempIntNum

    # 1페이지와 2페이지는 시작하면서 읽어내기 때문
    if totalPage >2 :
        crawlList(query)
        totalPageCount = totalPage - 2
        pageNo = 3

        while totalPageCount > 0 :
            if ((pageNo-1)%5) == 0: #arrow
                try:
                    clickElem = WebDriverWait(driver, delay) \
                        .until(EC.presence_of_element_located((By.ID, "info.search.page.next")))
                    clickElem.click()
                    time.sleep(1)
                    crawlList(query)
                except TimeoutException:
                    print("Loading took too much time. total page > 2!!!!")
                pageNo = 2
                totalPageCount -= 1
            else :  #now a arrow
                clickId = pagingString + str(pageNo)
                try:
                    clickElem = WebDriverWait(driver, delay) \
                        .until(EC.presence_of_element_located((By.ID, clickId)))
                    clickElem.click()
                    time.sleep(1)
                    crawlList(query)
                except TimeoutException:
                    print("Loading took too much time. total page > 2!!!!")
                pageNo += 1
                totalPageCount -= 1
    else :
        crawlList(query)





def printAllStores():
    global store_infos
    for e in store_infos:
        print(str(e.getName()) + " <---> " + str(e.getBranch()) + " <---> " + str(e.getPhoneNum()) + " <---> " + str(e.getAddress()))


def main():
    # init()
    global store_infos
    query = input("상호명을 입력하세요: ")
    if getCount(query) == True:  # 525개 이상의 데이터
        for i in range(0, len(c.cities)):
            locationQuery = c.cities[i]+query
            totalDataCount = getMapAndCrawlFirstPage(query, locationQuery)
            startCrawling(query, totalDataCount)
        printAllStores()
    else:  # 525개 미만의 데이터
        totalDataCount = getMapAndCrawlFirstPageUnder525(query)
        if totalDataCount > 15:
            startCrawling(query, totalDataCount)
            printAllStores()
        else:
            printAllStores()

if __name__ == "__main__":
    main()


