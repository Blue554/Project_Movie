import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random
from konlpy.tag import Okt
from multiprocessing import Process
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib import font_manager, rc
import matplotlib.font_manager as fm
import matplotlib
from wordcloud import WordCloud


# 씨네 21 평론가 리뷰 크롤링
def get_review(url):
    # 평론가 리뷰 크롤링
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    titles = str(soup.select('div.comment_area span.comment'))
    return titles

def remove_html(sentence) :
	sentence = re.sub('(<([^>]+)>)', '', sentence)
	return sentence

def cine21(number):
	url=f'http://www.cine21.com/movie/info/?movie_id={number}'
	titles = remove_html(get_review(url))
	print(titles)
	f = open("./d_critic/평론가리뷰.txt",'w')

	f.write(titles)
	f.close()

	nlp = Okt()
	message_N = nlp.nouns(titles)
	count = Counter(message_N)
	word_count = dict()

	for tag, counts in count.most_common(80):
    	 if (len(str(tag)) > 1):
        	word_count[tag] = counts
        	print("%s : %d" % (tag, counts))

	font_path = '/usr/share/fonts/nanum/NanumGothicBold.ttf'
	font_name = fm.FontProperties(fname=font_path).get_name()
	matplotlib.rc('font', family=font_name)
	fm._rebuild()

	plt.figure(figsize=(12, 5))
	plt.xlabel('키워드')
	plt.ylabel('빈도수')
	plt.grid(True)

	sorted_Keys = sorted(word_count, key=word_count.get, reverse=True)
	sorted_Values = sorted(word_count.values(), reverse=True)

	plt.bar(range(len(word_count)), sorted_Values, align='center')
	plt.xticks(range(len(word_count)), list(sorted_Keys), rotation='75')

	plt.show()

	wc = WordCloud(font_path, background_color='ivory', width=800, height=600)
	cloud = wc.generate_from_frequencies(word_count)

	plt.figure(figsize=(8, 8))
	plt.imshow(cloud)
	plt.axis('off')
	plt.show()

	cloud.to_file(f'd_critic/{number}_review_cloud.jpg')



cine21(56294)



