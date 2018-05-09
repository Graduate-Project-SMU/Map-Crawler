from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome("/Users/sml/chromedriver")
storeInfos = []

class storeInfoClass:
    def __init__(self):
        self.name = 0
        self.branch = 0
        self.phoneNum = 0
        self.address = 0
    def setName(self, name):
        self.name = name
    def setBranch(self, branch):
        self.branch = branch
    def setPhoneNum(self, phoneNum):
        self.phoneNum = phoneNum
    def setAddress(self, address):
        self.address = address
    def getName(self):
        return self.name
    def getBranch(self):
        return self.branch
    def getPhoneNum(self):
        return self.phoneNum
    def getAddress(self):
        return self.address
    

    



def initCrawler():
    #----------These are headless options-----------------
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    #Change Headless User-Agent to general User-Agent.
    TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome("/Users/sml/chromedriver", chrome_options=options)
    
    #-------------------------------------------------------

def getMap():
    driver.get("http://map.daum.net")
    elem = driver.find_element_by_name('q')
    elem.clear()
    elem.send_keys("스타벅스")
    elem.send_keys(Keys.RETURN)
    time.sleep(0.5)
    clickElem = driver.find_element(By.ID, "info.search.place.more")
    clickElem.click()
    time.sleep(0.5)

def startCrawling():
    # 1페이지에 15개의 정보!
    countStart = 0
    countEnd = 0
    _html=driver.page_source
    soup=BeautifulSoup(_html, "lxml")
    

    for e in soup.find_all("li", class_="PlaceItem"):
        tempClass = storeInfoClass()
        tempName = e.h6.a["title"]
        realName = tempName.split(" ")
        tempClass.setName(realName[0])
        tempClass.setBranch(realName[1])
        storeInfos.append(tempClass)
        countEnd += 1
    for i in range(countStart, countEnd):
        tempPhoneNums = []
        for e in soup.find_all("span", class_="phone"):
            tempPhoneNums.append(e.text)
        storeInfos[i].setPhoneNum(tempPhoneNums[i])
    for i in range(countStart, countEnd):
        tempAddresses = []
        for e in soup.find_all("p", class_="newAddress"):
            tempAddresses.append(e.text)
        storeInfos[i].setAddress(tempAddresses[i])
    
    for e in storeInfos:
        print(e.getName()+"***"+e.getBranch()+"***"+e.getPhoneNum()+"***"+e.getAddress())
#         print(e.h6.a["title"])
    


def main():
    getMap()
    startCrawling()
if __name__=="__main__":
    main()



#     driver.implicitly_wait(5)
#     location = '//*[@id="panel"]/div[2]/div[1]/div[2]/div[2]/div/div/a[1]'
#     clickElem = driver.find_element(By.XPATH, location)
#     clickElem.click()
    # clickElem.clear()
#     count = 0
#     while True:
#         clickElem = driver.find_element_by_class_name("next")
#         if clickElem:
#             clickElem.clear()
#             clickElem.click()
#             count += 1
#         else :
#             break;
    # print("count:" + count)
    #
    #_html=driver.page_source
#soup=BeautifulSoup(_html,"lxml")
#


#driver.quit()
