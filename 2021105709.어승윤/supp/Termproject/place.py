import requests
import sys
import re
from bs4 import BeautifulSoup

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

tempList_1 = soup.findAll('span', attrs={"class": "todaytemp"})
tempList_2 = soup.findAll('p', attrs={"class": "cast_txt"})
tempList_3 = soup.findAll('span', attrs={"class": re.compile("^lv")})
tempList_4 = soup.findAll('li', attrs={"class": "date_info today"})

try:
    tempList_1[1]
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