import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

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

def get_summary(review_list):
    star_list = []
    good_list = []
    bad_list = []

    for review in review_list:
        star_list.append(int(review.star))
        good_list.append(int(review.good))
        bad_list.append(int(review.bad))

    star_series = pd.Series(star_list)
    good_series = pd.Series(good_list)
    bad_series = pd.Series(bad_list)

    summary = pd.DataFrame({

        'Star ': star_series,
        'Good ': good_series,
        'Bad' : bad_series,
        'Score' : good_series/ (good_series+bad_series)
    })

    return summary


movie_code_list = [136900,167657,174321,184859,167391]

review_lists = []
for i in movie_code_list:
    title, review_list = crawl("https://movie.naver.com/movie/bi/mi/basic.nhn?code=" + str(i))
    summary = get_summary(review_list)
    print("[ %s ]" % (title))
    print(summary)
    review_lists.append((title, review_list))


matplotlib.rc('font',family="NanumBarunGothic")

def movie_compare(review_lists):
    count= 1
    x = []
    y = []
    for movie, review_list in review_lists:
        x.append(count)
        summary = get_summary(review_list)
        summary = summary[summary['Score'] > 0.8]
        y.append(summary['Star'].mean())
        count +=1
    plt.bar(x,y)
    plt.title('영화 별점 비교',fontproperties = fontprop)
    plt.xlabel('영화 번호', fontproperties=fontprop)
    plt.ylabel('신뢰성 별점 평균', fontproperties=fontprop)
    plt.show()
movie_compare(review_lists)




