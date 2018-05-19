# Map-Crawler

## Set virtual environment and install packages.

```
    $ conda create --name <project-name> python=3.6
    $ source activate <project-name>  // Mac or Linux
    $ pip install bs4
    $ pip install selenium
    $ pip install lxml
    $ pip install backports.csv
```

## Usage

```
    $ cd MapCrawler
    $ python main.py
```

## Notice

* (다음지도에 등록된)정확한 상호명을 입력해야 합니다.

* Chrome driver를 설치해야 합니다.
    * 링크 : [http://chromedriver.chromium.org/downloads](http://chromedriver.chromium.org/downloads)

* 입력을 받아 CSV파일(store.csv)을 생성합니다.

* 데이터가 525개 이상의 경우 도시 별 검색을 수행합니다.

* 현재 서울특별시 종로구, 중구에 대하여 검색만을 진행합니다. 범위를 조정하고 싶은 경우,
cities.py의 코드를 수정해주세요.

* 새로 데이터를 검색하는 경우, 기존의 CSV파일에 덧붙혀집니다.




## Development Tools

* Pycharm

* Anaconda3

* Python(version = 3.6)

* Chrome driver

* Excel
