# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import make_csv as m
import crawler_config as cc
import stores as s
import cities as c

delay = 0
driver = None
count_start = 0
count_end = 0
store_infos = []

#driver = webdriver.Chrome("/Users/sml/chromedriver")

def init():
    global driver
    driver = cc.initCrawler()

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
            if count.text == '':
                totCount = 0
            else:
                totCount = int(count.text, base=10)
            if totCount > 525:
                return True
            else:
                return False

def crawlList(query):
    print("now program crawls data....")
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
            tempClass.setName(realName[0].encode('euc-kr'))
            if len(realName) == 2:
                tempClass.setBranch(realName[1].encode('euc-kr'))
            else :
                tempClass.setBranch("".encode('euc-kr'))
            tempPhoneNum = e.find("span", class_="phone")
            tempClass.setPhoneNum(tempPhoneNum.text.encode('euc-kr'))
            tempAddress = e.find("span", class_="subAddress")
            if tempAddress != None:
                tempClass.setAddress(tempAddress.text.encode('euc-kr'))
            else :
                tempClass.setAddress("Unknown".encode('euc-kr'))
            store_infos.append(tempClass)
            count_end += 1
        else:
            continue
    count_start = count_end

def crawlListOver525(query):
    print("now program crawls data....")
    global count_start
    global count_end
    global store_infos
    _html = driver.page_source
    soup = BeautifulSoup(_html, "lxml")
    for e in soup.find_all("li", class_="PlaceItem"):
        tempClass = s.storeInfoClass()
        tempName = e.h6.a["title"]
        realName = tempName.split(" ")
        tfAddress = e.find("span", class_="subAddress")
        hasNotAddress= 1
        for i in range(0, len(store_infos)) :
            if tfAddress != None:
                if tfAddress.text == store_infos[i].getAddress().decode('euc-kr'):
                    hasNotAddress = 0
        if hasNotAddress and realName[0] == query:
            tempClass.setName(realName[0].encode('euc-kr'))
            if len(realName) == 2:
                tempClass.setBranch(realName[1].encode('euc-kr'))
            else :
                tempClass.setBranch("".encode('euc-kr'))
            tempPhoneNum = e.find("span", class_="phone")
            tempClass.setPhoneNum(tempPhoneNum.text.encode('euc-kr'))
            tempAddress = e.find("span", class_="subAddress")
            if tempAddress != None:
                tempClass.setAddress(tempAddress.text.encode('euc-kr'))
            else :
                tempClass.setAddress("Unknown".encode('euc-kr'))
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
        time.sleep(5)
        _html = driver.page_source
        soup = BeautifulSoup(_html, "lxml")
        count = soup.find("em", id="info.search.place.cnt")
        if count.text != '':
            total_data_count = int(count.text)
        else :
            total_data_count = 0
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

def getMapAndCrawlFirstPageOver525(query, locationQuery):
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
        if count.text != '':
            total_data_count = int(count.text)
        else :
            total_data_count = 0
        crawlListOver525(query)
        try:
            clickElem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.ID, "info.search.place.more")))
            clickElem.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")
        finally:
            return total_data_count

def startCrawlingUnder525(query, totalDataCount):
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

def startCrawlingOver525(query, totalDataCount):
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

    #2번째
    crawlListOver525(query)


    totalPageCount = totalPage - 2
    pageNo = 3

    while totalPageCount > 0 :
        if ((pageNo-1)%5) == 0: #arrow
            try:
                clickElem = WebDriverWait(driver, delay) \
                   .until(EC.presence_of_element_located((By.ID, "info.search.page.next")))
                clickElem.click()
                time.sleep(1)
                crawlListOver525(query)
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
                crawlListOver525(query)
            except TimeoutException:
                print("Loading took too much time. total page > 2!!!!")
            pageNo += 1
            totalPageCount -= 1

def printAllStores():
    for e in store_infos:
        print(str(e.getName()) + " <---> " + str(e.getBranch()) + " <---> " + str(e.getPhoneNum()) + " <---> " + str(e.getAddress()))



def main():
    init()
    continueTf = True
    while continueTf:
        global store_infos
        store_infos = []
        query = input("상호명을 입력하세요: ")
        if getCount(query) == True:  # 525개 이상의 데이터
            for i in range(0, len(c.cities)):
                locationQuery = c.cities[i]+query
                totalDataCount = getMapAndCrawlFirstPageOver525(query, locationQuery)
                startCrawlingOver525(query, totalDataCount)
        else:  # 525개 미만의 데이터
            totalDataCount = getMapAndCrawlFirstPageUnder525(query)
            if totalDataCount > 15:
                startCrawlingUnder525(query, totalDataCount)

        # printAllStores()
        # m.store_to_csv(store_infos)
        m.store_to_csv_pandas(store_infos)
        print("crawling data finish!")
        tf = input("검색을 계속 진행하시겠습니까? (y/n): ")
        if tf=='y':
            continueTf = True
        else:
            continueTf = False

if __name__ == "__main__":
    main()


