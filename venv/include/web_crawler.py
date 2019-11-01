import requests
from bs4 import BeautifulSoup

# 특정 URL에 접속하는 요청 Request객체 생성
request = requests.get('http://dowellcomputer.com/main.jsp')

# 접속한 이후의 웹 사이트 소스코드를 추출합니다.
html = request.text
# html소스코드를 파이썬 BeautifulSoup 객체로 변환합니다.
soup = BeautifulSoup(html,'html.parser')

# <a> 태그를 포함하는 요소를 추출합니다.
links = soup.select('td > a')
# print(links)
# 눌렀을 때 다른 링크로 이동 <a> 태그
# 모든 링크에 하나씩 접근합니다.
for link in links:
  #  링크가 href속성을 가지고 있다면
  if link.has_attr('href'):
    # href 속성의 값으로 notice라는 문자가 포함되어 있다면
    if link.get('href').find('notice') != -1:
      print(link.text)


# # 접속한 이후의 웹 사이트 소스코드 추출
# html = request.text.strip()
# # strip() 앞,뒤 공백이 제거됨
# print(html)

# option+command+i 개발자모드 - elements tab

