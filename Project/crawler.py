from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome("/Users/sml/chromedriver")
storeInfos = []
cities = [
        '서울특별시 강남구', '서울특별시 강동구', '서울특별시 강서구', '서울특별시 강북구', '서울특별시 관악구', '서울특별시 광진구', '서울특별시 구로구',
       '서울특별시 금천구', '서울특별시 노원구', '서울특별시 도봉구', '서울특별시 동대문구', '서울특별시 동작구', '서울특별시 마포구', '서울특별시 서대문구', 
       '서울특별시 서초구', '서울특별시 성북구', '서울특별시 성동구', '서울특별시 송파구', '서울특별시 양천구','서울특별시 영등포구', '서울특별시 용산구',
       '서울특별시 은평구', '서울특별시 종로구', '서울특별시 중구', '서울특별시 중랑구',
       '부산광역시 강서구', '부산광역시 금정구', '부산광역시 기장군', '부산광역시 남구', '부산광역시 동구', '부산광역시 동래구', '부산광역시 부산진구',
        '부산광역시 북구', '부산광역시 사상구', '부산광역시 사하구', '부산광역시 서구', '부산광역시 수영구', '부산광역시 연제구', '부산광역시 영도구',
        '부산광역시 중구', '부산광역시 해운대구',
        '대구광역시 남구', '대구광역시 달서구', '대구광역시 달성구', '대구광역시 동구', '대구광역시 북구', '대구광역시 서구', '대구광역시 수성구', '대구광역시 중구',
        '인천광역시 강화군', '인천광역시 계양구', '인천광역시 남구', '인천광역시 남동구', '인천광역시 동구', '인천광역시 부평구', '인천광역시 서구',
         '인천광역시 연수구', '인천광역시 옹진군',
        '광주광역시 광산구','광주광역시 남구','광주광역시 동구','광주광역시 북구','광주광역시 서구',
        '대전광역시 대덕구', '대전광역시 동구', '대전광역시 서구', '대전광역시 유성구', '대전광역시 중구',
        '울산광역시 남구','울산광역시 동구','울산광역시 북구','울산광역시 울주군','울산광역시 중구',
        '세종특별자치시',
        '경기도 가평군', '경기도 고양시', '경기도 과천시', '경기도 광명시', '경기도 광주시', '경기도 구리시', '경기도 군포시',
         '경기도 김포시', '경기도 남양주시', '경기도 동두천시', '경기도 부천시', '경기도 성남시', '경기도 수원시', '경기도 시흥시', '경기도 안산시',
         '경기도 안성시', '경기도 안양시', '경기도 양주시', '경기도 양평군', '경기도 여주시', '경기도 연천군', '경기도 오산시', '경기도 용인시',
         '경기도 의왕시', '경기도 의정부시', '경기도 이천시', '경기도 파주시', '경기도 평택시', '경기도 포천시', '경기도 하남시', '경기도 화성시',
        '강원도 강릉시', '강원도 고성군', '강원도 동해시', '강원도 삼척시', '강원도 속초시', '강원도 양구군', '강원도 양양군', '강원도 영월군',
        '강원도 원주시', '강원도 인제군', '강원도 정선군', '강원도 철원군', '강원도 춘천시', '강원도 태백시', '강원도 평창군', '강원도 홍천군',
        '강원도 화천군', '강원도 횡성군',
        '충청북도 괴산군', '충청북도 단양군', '충청북도 보은군', '충청북도 영동군', '충청북도 옥천군', '충청북도 음성군', '충청북도 제천시', '충청북도 증평군', 
        '충청북도 진천군', '충청북도 청주시', '충청북도 충주시',
        '충청남도 계룡시', '충청남도 공주시', '충청남도 금산군', '충청남도 논산시', '충청남도 당진시', '충청남도 보령시', '충청남도 부여군', '충청남도 서산시', 
        '충청남도 서천군', '충청남도 아산시', '충청남도 예산군','충청남도 천안시', '충청남도 청양군', '충청남도 태안군', '충청남도 홍성군', 
        '전라북도 고창군', '전라북도 군산시', '전라북도 김제시', '전라북도 남원시', '전라북도 무주군', '전라북도 부안군', '전라북도 순창군', '전라북도 완주군',
        '전라북도 익산시', '전라북도 임실군', '전라북도 장수군', '전라북도 전주시', '전라북도 정읍시', '전라북도 진안군',
        '전라남도 강진군', '전라남도 고흥군',  '전라남도 곡성군',  '전라남도 광양시', '전라남도 구례군',  '전라남도 나주시',  '전라남도 담양군',  '전라남도 목포시',  
        '전라남도 무안군',  '전라남도 보성군',  '전라남도 순천시',  '전라남도 신안군',  '전라남도 여수시',  '전라남도 영광군',  '전라남도 영암군',   '전라남도 완도군', 
        '전라남도 장성군', '전라남도 장흥군','전라남도 진도군','전라남도 함평군', '전라남도 해남군', '전라남도 화순군',
        '경상북도 경산시', '경상북도 경주시', '경상북도 고령군', '경상북도 구미시', '경상북도 군위군', '경상북도 김천시', '경상북도 문경시', '경상북도 봉화군', '경상북도 상주시',
        '경상북도 성주군', '경상북도 안동시', '경상북도 영덕군', '경상북도 영양군', '경상북도 영주시', '경상북도 영천시', '경상북도 예천군', '경상북도 울릉군', '경상북도 의성군', 
        '경상북도 청도군', '경상북도 청송군','경상북도 칠곡군','경상북도 포항시',
        '경상남도 거제시', '경상남도 거창군', '경상남도 고성군', '경상남도 김해시', '경상남도 남해군', '경상남도 밀양시', '경상남도 사천시', '경상남도 산청군', '경상남도 양산시', 
        '경상남도 의령군', '경상남도 진주시', '경상남도 창녕군', '경상남도 창원시', '경상남도 통영시', '경상남도 하동군', '경상남도 함안군',
        '경상남도 함양군', '경상남도 합천군',
        '제주특별자치도 제주시', '제주특별자치도 서귀포시'
       ]

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

def getCount(query):
    driver.get("http://map.daum.net")
    delay = 2 # seconds
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
        if len(count.text)>3:
            return True
        else :
            if int(count.text) > 524:
                return True
            else:
                return False

def getMapOnce(query):
    driver.get("http://map.daum.net")
    delay = 2 # seconds
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
        print(count)
        try: 
            clickElem = WebDriverWait(driver, delay)\
            .until(EC.presence_of_element_located((By.ID, "info.search.place.more")))
            clickElem.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")

    
def startCrawling(query):
    # ******1페이지에 15개의 정보!******
    pageNo = 2
    countStart = 0
    countEnd = 0
    _html=driver.page_source
    soup=BeautifulSoup(_html, "lxml")
    
    for e in soup.find_all("li", class_="PlaceItem"):
        tempClass = storeInfoClass()
        tempName = e.h6.a["title"]
        realName = tempName.split(" ")
        if realName[0] == query:
            tempClass.setName(realName[0])
            tempClass.setBranch(realName[1])
            storeInfos.append(tempClass)
            countEnd += 1
        else:
            continue
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
    countStart = countEnd
  

    '''
      page = soup.find("a", id="info.search.page.no2")
      while page.text != None:
    '''
        
        
        
    for e in storeInfos:
        print(e.getName()+"***"+e.getBranch()+"***"+e.getPhoneNum()+"***"+e.getAddress())


def main():
    query = input("상호명을 입력하세요: ")
    if getCount(query) == True:     #525개 이상의 데이터
        print("A lot!")
    else:        #525개 미만의 데이터
        getMapOnce(query)
        startCrawling(query)
if __name__=="__main__":
    main()


