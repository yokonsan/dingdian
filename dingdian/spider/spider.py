# -*- coding:utf-8 -*-
import re
import time
import requests
from requests.exceptions import ConnectionError


def parse_url(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    }
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            # 处理一下网站打印出来中文乱码的问题
            resp.encoding = 'utf-8'
            return resp.text
        return None
    except ConnectionError:
        print('Error.')
    return None

def get_index_result(resp):
    resp = re.sub(r'<em>','',resp)
    resp = re.sub(r'</em>','',resp)
    p = re.compile(r'<a cpos="img".*?<img src="(.*?)".*?<a cpos="title".*?="(.*?)".*?_blank">'
                   + r'(.*?)</a>.*?<p class="result-game-item-desc">(.*?)'
                   + r'</p>.*?<span.*?<span>(.*?)</span>.*?title">(.*?)</span>.*?title">(.*?)</span>', re.S)
    items = re.findall(p, resp)
    for i in items:
        data = {
            'image': i[0],
            'url': i[1],
            'title':i[2].strip(),
            'profile':i[3].strip().replace('\u3000','').replace('\n',''),
            'author': i[4].strip(),
            'style': i[5].strip(),
            'time': i[6].strip()
        }
        yield data

def get_chapter(resp):
    p = re.compile(r'<dd> <a style=.*?href="(.*?)">(.*?)</a></dd>')
    chapters = re.findall(p, resp)
    for i in chapters:
        data = {
            'url': i[0],
            'chapter': i[1]
        }
        yield data

def get_article(resp):
    p = re.compile(r'<div id="content">(.*?)</div>', re.S)
    article = re.findall(p, resp)[0]
    # 文章中的'<br/>'标签先不去除，后面有用
    print(article.strip().replace('&nbsp;',''))


def main(search, page=0):
    t1 = time.time()
    url = 'http://zhannei.baidu.com/cse/search?q={search}&p={page}&s=1682272515249779940'.format(search=search,page=page)
    text = parse_url(url)
    get_index_result(text)
    data = get_index_result(text)
    # for i in data:

    url = data.__next__()['url']
    print(url)
    resp = parse_url(url)
    result = get_chapter(resp)
    chapter_url = url + result.__next__()['url']
    print(chapter_url)
    html = parse_url(chapter_url)
    get_article(html)
    print(time.time() - t1)

main('诛仙')

