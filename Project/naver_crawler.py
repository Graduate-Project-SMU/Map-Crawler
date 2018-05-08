
# coding: utf-8

# In[50]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def readNaverMap():
    #----------These are headless options-----------------
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")

    #Change Headless User-Agent to general User-Agent.
    # TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'
    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    # driver = webdriver.Chrome("/Users/sml/chromedriver", chrome_options=options)
    #-------------------------------------------------------
    driver = webdriver.Chrome("/Users/sml/chromedriver")
    driver.get("https://map.naver.com/")
    elem = driver.find_element_by_id("search-input")
    elem.clear()
    elem.send_keys("상명대학교")
    elem.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)
    location = '//*[@id="panel"]/div[2]/div[1]/div[2]/div[2]/div/div/a[1]'
    clickElem = driver.find_element(By.XPATH, location)
    clickElem.click()
    # clickElem.clear()
    # count = 0
    # while True:
    #     clickElem = driver.find_element_by_class_name("next")
    #     if clickElem:
    #         clickElem.clear()
    #         clickElem.click()
    #         count += 1
    #     else :
    #         break;
    # print("count:" + count)
    #
    #_html=driver.page_source
    #soup=BeautifulSoup(_html,"lxml")
    #


    #driver.quit()

def main():
    readNaverMap()

if __name__ == "__main__":
    main()

