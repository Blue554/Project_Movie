#/usr/bin/env python3
import json
import re
import datetime
from konlpy.tag import Okt

from collections import Counter

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud

d_today = datetime.date.today()
yesterday = d_today - datetime.timedelta(1)
d_date = yesterday.strftime("%Y%m%d")


inputFileName = './naver_review/'+d_date+'_naver_review'
data = json.loads(open(inputFileName+'.json', 'r', encoding='utf-8').read())


message = ''


for item in data:
 if item['movie'] == "올빼미":
  a = item['movie']
  if 'sentence' in item.keys(): 
   message = message + re.sub(r'[^\w]|영화', ' ', str(item['sentence'])) +''
        
nlp = Okt()
message_N = nlp.nouns(message) 


count = Counter(message_N)


word_count = dict()

for tag, counts in count.most_common(80):
    if(len(str(tag))>1):
        word_count[tag] = counts
        print("%s : %d" % (tag, counts))


import matplotlib.font_manager as fm
font_path = '/usr/share/fonts/nanum/NanumGothicBold.ttf'
font_name = fm.FontProperties(fname = font_path).get_name()
matplotlib.rc('font', family=font_name)
fm._rebuild()

plt.figure(figsize=(12,5))
plt.xlabel('키워드')
plt.ylabel('빈도수')
plt.grid(True)

sorted_Keys = sorted(word_count, key=word_count.get, reverse=True)
sorted_Values = sorted(word_count.values(), reverse=True)

plt.bar(range(len(word_count)), sorted_Values, align='center')
plt.xticks(range(len(word_count)), list(sorted_Keys), rotation='75')

plt.show()

wc = WordCloud(font_path, background_color='ivory', width=800, height=600)
cloud=wc.generate_from_frequencies(word_count)

plt.figure(figsize=(8,8))
plt.imshow(cloud)
plt.axis('off')
plt.show()

d_date = datetime.date.today().strftime("%Y%m%d")

cloud.to_file(f'wordcloud/{a}{d_date}_cloud.jpg')
