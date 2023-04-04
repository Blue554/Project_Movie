#/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import time
import csv
import datetime
import os
d_today = datetime.date.today()
yesterday = d_today - datetime.timedelta(1)
d_date = d_today.strftime("%Y%m%d")

rz = "d_naver_review"

count = 0
need_reviews_cnt = 100
reviews = []
review_data = []
for page in range(1, 10):
    url = f'https://movie.naver.com/movie/point/af/list.naver?&page={page}'
    html = requests.get(url)
    
    soup = BeautifulSoup(html.content, 'html.parser')
    
    reviews = soup.find_all("td", {"class": "title"})

    for review in reviews:
       sentence = review.find("a", {"class": "report"}).get("onclick").split("', '")[2]
       if sentence != "":
            movie = review.find("a", {"class": "movie color_b"}).get_text()
            score = review.find("em").get_text()
            review_data.append([movie, sentence, int(score)])
            need_reviews_cnt -= 1
    if need_reviews_cnt < 0:
        break
    time.sleep(0.5)

print(count)


try:
    if not os.path.exists(rz):
        os.makedirs(rz)
except OSError:
    print("Error: Cannot create the directory {}".format(savePath))



columns_name = ["movie", "sentence", "score"]
with open("./d_naver_review/"+d_date+"_naver_review.csv", "w", newline="", encoding='utf8') as f:
    write = csv.writer(f)
    write.writerow(columns_name)
    write.writerows(review_data)

