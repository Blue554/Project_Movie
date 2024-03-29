# -*- coding: utf-8 -*-
"""movie_rank.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Blue554/Project_Movie/blob/main/movie_rank.ipynb

코드 1. 필요 패키지 및 드라이버 설치
"""

import requests
import json
import pandas as pd
import datetime

"""코드 2. (어제)영화 순위 가져오기 및 api key 등록"""

d_today = datetime.date.today()
yesterday = d_today - datetime.timedelta(1)
d_date = yesterday.strftime("%Y%m%d")
movie_key = "ee7bfcd03b5a6ce684caeac3a084b73a"

"""코드3. url 접속 및 text가져오기"""

url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={movie_key}&targetDt={d_date}'
res = requests.get(url)
text = res.text

"""코드4. 영화 순위 가져오기

"""

d = json.loads(text)
movie = []
for b in d['boxOfficeResult']['dailyBoxOfficeList']:
    movie.append([b['rank'], b['movieNm']])
data = pd.DataFrame(movie)
data.to_csv("movie_rank.txt", mode='w', encoding='utf-8', index=False)
