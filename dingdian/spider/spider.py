# coding=utf-8
import re
import requests
from requests.exceptions import ConnectionError


"""
爬虫api：
    搜索结果页：get_index_result(search)
    小说章节页：get_chapter(url)
    章节内容：get_article(url)
"""
class DdSpider(object):

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}

    def parse_url(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                # 处理一下网站打印出来中文乱码的问题
                resp.encoding = 'utf-8'
                return resp.text
            return None
        except ConnectionError:
            print('Error.')
        return None

    # 搜索结果页数据
    def get_index_result(self, search, page=0):
        url = 'http://zhannei.baidu.com/cse/search?q={search}&p={page}&s=1682272515249779940&entry=1'.format(
            search=search, page=page)
        resp = self.parse_url(url)
        resp = re.sub(r'<em>', '', resp)
        resp = re.sub(r'</em>', '', resp)
        p = re.compile(r'<a cpos="img".*?<img src="(.*?)".*?<a cpos="title".*?="(.*?)".*?_blank">'
                       + r'(.*?)</a>.*?<p class="result-game-item-desc">(.*?)'
                       + r'</p>.*?<span.*?<span>(.*?)</span>.*?title">(.*?)</span>.*?title">(.*?)</span>', re.S)
        items = re.findall(p, resp)
        for i in items:
            data = {
                'image': i[0],
                'url': i[1],
                'title': i[2].strip(),
                'profile': i[3].strip().replace('\u3000', '').replace('\n', ''),
                'author': i[4].strip(),
                'style': i[5].strip(),
                'time': i[6].strip()
            }
            yield data

    # 小说章节页数据
    def get_chapter(self, url):
        resp = self.parse_url(url)
        p = re.compile(r'<dd> <a style=.*?href="(.*?)">(.*?)</a></dd>')
        chapters = re.findall(p, resp)
        for i in chapters:
            data = {
                'url': str(url) + i[0],
                'chapter': i[1]
            }
            yield data

    # 章节内容页数据
    def get_article(self, url):
        resp = self.parse_url(url)
        p = re.compile(r'<div id="content">(.*?)</div>', re.S)
        article = re.findall(p, resp)
        # 文章中的'<br/>'标签先不去除，后面在模版中使用
        return article[0].strip()

# dd = DdSpider()
# print(dd.get_article('http://www.23us.cc/html/158/158120/8275025.html'))

