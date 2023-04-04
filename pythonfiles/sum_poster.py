from bs4 import BeautifulSoup
import requests
import os

import threading
from multiprocessing import Process

savePath = r'./'

def getMovieInfo(movie_code):
    global savePath

    delim = '\t'
    f = open(os.path.join(savePath, f'{movie_code}.csv'), 'w', encoding='UTF-8')
    f.write('story' + delim + '\n')

    t = threading.Thread(target=getImage, args=(os.path.join(savePath, str(movie_code)), str(movie_code)))
    t.start()
    url = f'https://movie.naver.com/movie/bi/mi/point.naver?code={movie_code}'
    response = requests.get(url)

    if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')

            title = soup.find('head').find('title').text.replace(' : 네이버 영화', '')
            story = getStory(f'https://movie.naver.com/movie/bi/mi/basic.naver?code={movie_code}')
            if story:
               	f.write(story)
    f.close()


def getStory(url):
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        story = soup.find('p', 'con_tx')
        if story is not None:
            story = str(story).replace('<p class="con_tx">', '').replace('</p>', '').replace('\n', '').replace('\t', '')
            story = str(story).replace('&lt;', '<').replace('&gt;', '>').replace('\r', '').replace('\xa0', '')
            story = str(story).replace('<br/>', '')

            return str(story)
        return False
    else:
        print(response.status_code)


def getImage(path, codes):
    if not os.path.isdir(os.path.join(path)):
        os.makedirs(path)
        url = f'https://movie.naver.com/movie/bi/mi/photoViewPopup.naver?movieCode={codes}'
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            imgUrl = soup.find('img', id='targetImage')
            if imgUrl is not None:
                imgUrl = imgUrl.attrs['src']
                with open(os.path.join(path, codes + '.png'), 'wb') as poster:
                    poster.write(requests.get(imgUrl).content)
        else:
            print(response.status_code)


if __name__ == "__main__":
    p1 = Process(target=getMovieInfo(74977))
    p2 = Process(target=getMovieInfo(191430))
    p3 = Process(target=getMovieInfo(190694))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
