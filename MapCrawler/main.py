from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import init_crawler
import stores
import cities


driver = webdriver.Chrome("/Users/sml/chromedriver")
count_start = 0
count_end = 0




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

def crawlList(query):
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
            tempPhoneNum = e.find("span", class_="phone")
            tempClass.setPhoneNum(tempPhoneNum.text)
            tempAddress = e.find("span", class_="subAddress")
            tempClass.setAddress(tempAddress.text)
            stores.storeInfos.append(tempClass)
            count_end += 1
        else:
            continue
    count_start = count_end

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
        crawlList(query)
        try:
            clickElem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.ID, "info.search.place.more")))
            clickElem.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")
        finally:
            return totalDataCount




def startCrawling(query, totalDataCount):
    # ******1페이지에 15개의 정보!******
    global count_start
    global count_end
    pagingString = "info.search.page.no"
    tempFloatNum = float(totalDataCount/15)
    tempIntNum = int(totalDataCount/15)
    totalPage = tempIntNum + 1
    remainder = int((tempFloatNum - float(tempIntNum))*10)


    # 1페이지와 2페이지는 시작하면서 읽어내기 때문
    if totalPage >2 :
        crawlList(query)
        pageNo = 3
        while pageNo <= totalPage:
            
        # if totalPage < 5:
        #     maxCount = 3
        #     idx = 0
        #     while idx < maxCount:
        #         pagingString += str(idx+3)
        #         idx += 1
        # else :
        #     firstMaxCount = 3
        #     maxCount = 4
        #     idx = 0
    else :
        crawlList(query)



def printAllStores():
    for e in stores.storeInfos:
        print(e.getName() + "***" + e.getBranch() + "***" + e.getPhoneNum() + "***" + e.getAddress())


def main():
    # init_crawler.initCrawler()
    query = input("상호명을 입력하세요: ")
    if getCount(query) == True:  # 525개 이상의 데이터
        print("A lot of datas!")
    else:  # 525개 미만의 데이터
        totalDataCount = getMapAndCrawlFirstPage(query)
        if totalDataCount > 15:
            startCrawling(query, totalDataCount)
            printAllStores()
        else:
            printAllStores()

if __name__ == "__main__":
    main()


