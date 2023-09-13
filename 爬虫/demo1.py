import requests
from bs4 import BeautifulSoup
import re
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'
}
index = 0

# print(response.status_code)
res = []

titile = re.compile(r'<span class="title">(.*?)</span>')
actors = re.compile(r'<p class="">(.*?)<br/>', re.S)
type = re.compile(r'<br/>(.*?)</p>', re.S)
comment = re.compile(r'<span class="inq">(.*?)</span>')
# t = re.compile(r'<p class="">(.*?)</p>', re.S)

while index < 250:
    response = requests.get(f'https://movie.douban.com/top250?start={index}&filter=', headers=headers)
    if response.ok:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        soup = soup.find_all('div', class_='info')
        for item in soup:
            item = str(item)
            movie = {}
            # item.replace('\t','')
            # item.replace('\n','')
            movie['title'] = re.findall(titile, item)[0]
            movie['actors'] = re.findall(actors, item)[0].replace(' ', '').replace('\n', '').replace('\xa0', '')
            movie['type'] = re.findall(type, item)[0].replace(' ', '').replace('\n', '').replace('\xa0', '')
            if len(re.findall(comment, item))>0:
                movie['comment'] = re.findall(comment, item)[0]
            else:
                movie['comment'] = []
            res.append(movie)
            index += 1
    else:
        print('请求失败')

for i in res:
    print(i)