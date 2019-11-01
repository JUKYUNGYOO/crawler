import urllib.request
from bs4 import BeautifulSoup


class Review:
    def __init__(self, comment, date, star, good, bad):
        self.comment = comment
        self.date = date
        self.star = star
        self.good = good
        self.bad = bad

    def show(self):
        print("내용:" + self.comment +
              "\n날짜:" + self.date +
              "\n별정:" + self.star +
              "\n좋아요:" + self.good +
              "\n싫어요:" + self.bad)
def crawl(url):
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    review_list = []
     # h_movie 클래스의 h3 태그에 포함되어 있는 a태그를 찾아서
    title = soup.find('h3', class_='h_movie').find('a').text.strip()
      # div클래스 의 score_result 클래스
    div = soup.find("div", class_="score_result")
    data_list = div.select("ul > li")
# ul 태그에 포함되어 있는 li 태그

    for review in data_list:
        star = review.find("div", class_="star_score").text.strip()
        reply = review.find("div", class_="score_reple")
        comment = reply.find("p").text.strip()
         # dt태그안에 em태그의 두번째가 날짜
        date = reply.select("dt > em")[1].text.strip()
        button = review.find("div", class_="btn_area")
        sympathy = button.select("a > strong")
        good = sympathy[0].text
        bad = sympathy[1].text
        review_list.append(Review(comment, date, star, good, bad))

    return title, review_list
title, review_list = crawl('https://movie.naver.com/movie/bi/mi/basic.nhn?code=36944')
print('제목:' + title)
for review in review_list:
    review.show()

