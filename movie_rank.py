#/usr/bin/python3
import requests
import json
import pandas as pd
import datetime
import os

d_today = datetime.date.today()
yesterday = d_today - datetime.timedelta(1)
d_date = yesterday.strftime("%Y%m%d")
movie_key = "ee7bfcd03b5a6ce684caeac3a084b73a"


url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={movie_key}&targetDt={d_date}'
res = requests.get(url)
text = res.text


d = json.loads(text)
movie = []
for b in d['boxOfficeResult']['dailyBoxOfficeList']:
    movie.append([b['rank'], b['movieNm'],b['openDt']])
data = pd.DataFrame(movie)

savePath = "./movie_rank"

try:
    if not os.path.exists(savePath):
        os.makedirs(savePath)
except OSError:
    print("Error: Cannot create the directory {}".format(savePath))
data.to_csv(savePath+"/"+d_date+"_movie_rank.txt", mode='w', encoding='utf-8', index=False)
