import requests
import sys
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import parse

# 장소의 날씨 정보 찾기
location = input('데이트 할 지역을 입력해주세요 : ')
Time = int(input('내일 날씨를 원하시면 1, 모레 날씨를 원하시면 2를 입력해주세요 : '))

if Time == 1:
    Time = '내일'
elif Time == 2:
    Time = '모레'
else:
    print('1또는 2를 입력했는지 확인해주세요.' + "\n" + "프로그램을 재시작 해주세요.")
    sys.exit()

enc_location = location + Time + '+날씨'

url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="+ enc_location

res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

tempList_1 = soup.findAll('span', attrs={"class": "todaytemp"}) #기온
tempList_2 = soup.findAll('p', attrs={"class": "cast_txt"}) #날씨
tempList_3 = soup.findAll('span', attrs={"class": re.compile("^lv")}) #미세먼지
tempList_4 = soup.findAll('li', attrs={"class": "date_info today"}) #강수확률

try:
    tempList_1[1] #검색결과가 없으면 여기서 오류가 발생
except:
    print("-" * 200)
    print("검색 결과가 없습니다. 지역을 잘 입력했는지 확인해주세요." +  "\n" + '만약 제대로 지역을 검색하셨다면 조금 더 큰 행정단위로 지역을 입력해주세요.' + "\n" + "프로그램을 재시작 후 지역을 다시 입력해주세요.")
    sys.exit()


if Time == '내일':
    Morning_Temperature = tempList_1[1].text
    Morning_Weather = tempList_2[1].text
    Morning_Fine_dust = tempList_3[1].text
    Morning_Rain_rate = tempList_4[1].findAll('span', attrs={"class": "num"})[0].text
    Afternoon_Temperature = tempList_1[2].text
    Afternoon_Weather = tempList_2[2].text
    Afternoon_Fine_dust = tempList_3[2].text
    Afternoon_Rain_rate = tempList_4[1].findAll('span', attrs={"class": "num"})[1].text


else:
    Morning_Temperature = tempList_1[3].text
    Morning_Weather = tempList_2[3].text
    Morning_Fine_dust = tempList_3[3].text
    Morning_Rain_rate = tempList_4[2].findAll('span', attrs={"class": "num"})[0].text
    Afternoon_Temperature = tempList_1[4].text
    Afternoon_Weather = tempList_2[4].text
    Afternoon_Fine_dust = tempList_3[4].text
    Afternoon_Rain_rate = tempList_4[2].findAll('span', attrs={"class": "num"})[1].text

print("-"*200)
print([Time+'날씨'])
print("오전 기온 : " + Morning_Temperature + "°C" + "\t"*4 + "오후 기온 : " + Afternoon_Temperature + "°C")
print("오전 날씨 : " + Morning_Weather + "\t"*4 + "오후 날씨 : " + Afternoon_Weather)
print("오전 미세먼지 : " + Morning_Fine_dust + "\t"*4 + "오후 미세먼지 : " + Afternoon_Fine_dust)
print("오전 강수확률 : " + Morning_Rain_rate + "%" + "\t"*4 + "오후 강수확률 : " + Afternoon_Rain_rate + "%")

 # 강수확률, 미세먼지에 따른 멘트 설정
if int(Morning_Rain_rate) > 49 and int(Afternoon_Rain_rate) > 49:
    if Morning_Fine_dust == re.compile("^나쁨") and Afternoon_Fine_dust == re.compile("^나쁨"):
        print(Time + " 하루종일 미세먼지도 안 좋고 비 올 확률이 있어 야외 데이트는 좋지 않아요.")
    elif Morning_Fine_dust == re.compile("^나쁨"):
        print(Time + " 오전에 미세먼지가 안 좋고 하루종일 비 올 확률이 있어 야외 데이트는 좋지 않아요")
    elif Afternoon_Fine_dust == re.compile("^나쁨"):
        print(Time + " 오후에 미세먼지가 안 좋고 하루종일 비 올 확률이 있어 야외 데이트는 좋지 않아요")
    else:
        print(Time + " 하루종일 비 올 확률이 있어 야외 데이트는 별로 좋지 않아요")

elif int(Morning_Rain_rate) > 49 :
    if Morning_Fine_dust == re.compile("^나쁨") and Afternoon_Fine_dust == re.compile("^나쁨"):
        print(Time + " 하루종일 미세먼지도 안 좋고 오전에 비 올 확률이 있어 야외 데이트는 좋지 않아요.")
    elif Morning_Fine_dust == re.compile("^나쁨"):
        print(Time + " 오전에 미세먼지가 안 좋고 비 올 확률이 있어 오후에 데이트 하는 것을 추천드려요")
    elif Afternoon_Fine_dust == re.compile("^나쁨"):
        print(Time + " 오후에 미세먼지가 안 좋고 오전에 비 올 확률이 있어 야외 데이트는 좋지 않아요")
    else:
        print(Time + " 오전에 비 올 확률이 있어 오후에 데이트 하는 것을 추천드려요")

elif int(Afternoon_Rain_rate) > 49:
    if Morning_Fine_dust == re.compile("^나쁨") and Afternoon_Fine_dust == re.compile("^나쁨"):
        print(Time + " 하루종일 미세먼지도 안 좋고 오후에 비 올 확률이 있어 야외 데이트는 좋지 않아요.")
    elif Morning_Fine_dust == re.compile("^나쁨"):
        print(Time + " 오전에 미세먼지가 안 좋고 오후에 비 올 확률이 있어 야외 데이트는 별로 좋지 않아요")
    elif Afternoon_Fine_dust == re.compile("^나쁨"):
        print(Time + " 오후에 미세먼지가 안 좋고 비 올 확률이 있어 오전에 데이트 하는 것을 추천드려요.")
    else:
        print(Time + " 오후에 비 올 확률이 있어 오전에 데이트 하는 것을 추천드려요")

else:
    print("데이트 하기 완벽한 날씨에요!")

print("-" * 200)

choice = input('데이트 정보를 원하시면 1, 원하시지 않으면 엔터를 눌러주세요 : ')

if choice != '1':
    print("-"*200)
    print('날씨 좋은 날 더 즐거운 데이트 하시길 바래요!' + '\n' + '다른 지역의 정보를 알고 싶으시면 프로그램을 재시작 해주세요.'  )
    sys.exit()

else:
    print("-" * 200)
    print("잠시만 기다려주세요")
    print("-" * 200)


# 데이트 장소 정보 찾기 (구글에 검색)
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

 # 가져온 데이터를 정리
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
