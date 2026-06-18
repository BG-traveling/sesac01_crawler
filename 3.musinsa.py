#라이브러리
#인터넷 요청 -> requests
#정적 웹페이지 -> beautifulsoup4
#동적 웹페이지 -> selenium
import requests
from bs4 import BeautifulSoup


#웹 브라우저 통신(크롬)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


#시간 -> 웹페이지를 기다릴 시간 명시적으로 표현
import time
from tqdm import tqdm

#판다스로 데이터 저장
import pandas as pd

#크롬 드라이버의 옵션
option = Options()
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('--disble-gpu')
option.add_argument('--enable-unsafe-swiftshader')

#동적인 일들을 수행하는 '웹 드라이버'
driver = webdriver.Chrome(options=option)
base_url = 'https://www.musinsa.com/categories/item/001'

driver.get(base_url)
time.sleep(2)

#스크롤을 내려야 모든 이미지와 요소가 로딩이 됨
driver.execute_script('window.scrollTo(0, 2000)')
time.sleep(2)

#창에 보이는 아이템 가져오기
#정적(bs4), 동적(selenium) .find('구분자')
#html => 웹페이지 '내용' 담당, CSS => 웹페이지 "디자인" 담당
items = driver.find_elements(By.CSS_SELECTOR, ".sc-bSFBcf.iEkOIH")
item_list = []

for item in items:
    #아래의 코드를 실행해봐!
    try :
        #개별 상품에 대한 정보를 get
        #find_element(CSS를 기준으로 찾아줘, a['이름']) : '이름'을 가지고 있는 블럭
        #find_element <- 작은 범위에서 데이터를 찾아오겠다! / driver.find_elements
        #a태그가 붙은['이름']을 가진것
        a_tag = item.find_element(By.CSS_SELECTOR, "a[data-original-price]")

        #상품 이름
        name = a_tag.get_attribute("aria-label")
        #예외처리
        # str(name) -> name에 뭐가 들어오든 str처리
        # replace -> "제거할 데이터", ""
        # strip -> 양쪽 공백 제거
        name = (str(name).replace('상품상세로 이동', '').strip() if name else "이름없음")

        #브랜드 이름
        brand = a_tag.get_attribute("data-item-brand")
        brand = str(brand).strip() if brand else "브랜드 없음"

        #가격//data-best-price
        price = a_tag.get_attribute("data-price")
        price = str(price).strip() if price else "가격 없음"

        #상세페이지
        #href(html에서 '하이퍼링크'를 의미, 이미지/미디어로 연결되는 태그 href)
        link = a_tag.get_attribute("href")
        link = str(link).strip() if link else "링크없음"
        # print(f'''name : {name},
        #         brand : {brand},  
        #         price : {price},
        #         link  : {link}   ''')

        item_list.append({
            '상품명': name,
            '브랜드': brand,
            '가격': price,
            '상품링크': link
        })

    #실행하다가 '에러'가 발생하면 이렇게 해~ (예외처리)
    except Exception as e:
        print(f'에러가 발생했습니다. :{e}')

#드라이버 종료
driver.quit()

df = pd.DataFrame(item_list)
df.to_csv('./musinsa_result.csv', index=False,encoding='utf-8-sig')