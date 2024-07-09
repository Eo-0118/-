import requests
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import parse

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome('/Users/eoseung-yun/Desktop/chromedriver',options=options)
driver.get("https://www.google.com")
elem = driver.find_element_by_name("q")
elem.send_keys(location + " 가볼만한 곳")
elem.send_keys(Keys.RETURN)
driver.find_element_by_css_selector(".MXl0lf.mtqGb").click()

try:
    driver.find_elements_by_css_selector(".VfPpkd-vQzf8d")[1].click()
except:
    print("제대로 검색 되지 않습니다. 조금 더 큰 행정단위로 지역을 입력해주세요." + "\n" + "프로그램을 재시작 후 지역을 다시 입력해주세요.")
    sys.exit()

driver.find_elements_by_css_selector(".VfPpkd-vQzf8d")[1].click()
place_url = driver.current_url

# 데이트 장소 정보 찾기 (구글에 나온정보 크롤링)
res = requests.get(place_url)
res.raise_for_status()
html = res.text
html = res.content.decode('utf-8','replace')
soup = BeautifulSoup(html, "lxml")

places = soup.findAll('div', attrs={"class": "Ld2paf"})

try:
    places[0]
except:
    print("검색 결과가 없습니다. 지역을 잘 입력했는지 확인해주세요." + "\n" + '만약 제대로 지역을 검색하셨다면 조금 더 큰 행정단위로 지역을 입력해주세요.' + "\n" + "프로그램을 재시작 후 지역을 다시 입력해주세요.")
    sys.exit()

rate_list = []
place_list = []
for place in places:

    temptuple = ()

    name = place.find('div', attrs={"class": "skFvHc"}).get_text()

    rate = place.find('span', attrs={"class": "KFi5wf lA0BZ"})
    if rate:
        rate = rate.get_text()
        temp_rate = rate.replace(".", "")
        temp_rate = int(temp_rate)
    else:
        rate = "0"

    comment_cnt = place.find('span', attrs={"class": "jdzyld XLC8M"})
    if comment_cnt:
        comment_cnt = comment_cnt.get_text()
        comment_cnt = comment_cnt.replace(",","")
        comment_cnt = int(comment_cnt[2:-1])

    else:
        comment_cnt = 0

    # 장소에 대한 url을 오류가 나지 않는 url형식으로 바꾸기
    choice_place_url_tmp = "map.naver.com/v5/search/" + name
    choice_place_url = "http://" + parse.quote(choice_place_url_tmp)

    temptuple = (name, rate, comment_cnt, choice_place_url)
    place_list.append(temptuple)

# 별점이 높은 순서로 나열하고 동일 별점일 경우 댓글수를 비교해 10개의 장소를 선택
place_list.sort(key=lambda x: (x[1],x[2]))
place_list.reverse()

print('[데이트 추천 장소 Top 10]' + "\n" + "장소   /  별점   /   댓글수   /   장소 관련 정보 더보기")
for i in range(10):
    print(place_list[i])
print("-" * 200)

more_inf = input("더 많은 추천 장소를 원하시면 1, 원하시지 않으면 엔터를 눌러주세요. :")
if more_inf == '1':
    print("-" * 200)
    if len(place_list) > 21:
        for j in range(10, 21):
            print(place_list[j])
    else:
        for j in range(10,len(place_list)):
            print(place_list[j])

print("-" * 200)
print("장소를 참조하여 즐거운 데이트 되세요!")