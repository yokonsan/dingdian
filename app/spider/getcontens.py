import requests
from bs4 import BeautifulSoup
from .spider import get_search_url, info_list


# 获取页面的response然后返回
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    html = requests.get(url,headers=headers).content

    return html

def get_allbook_url(search_name):
    info = []
    for item in info_list.find():
        if search_name in item:
            info = item[search_name]
    if info ==[]:
        info = get_search_url(search_name)
    urls = [i[0] for i in info]
    # print(urls)
    return urls


def get_allzj_title(search_name):

    urls = get_allbook_url(search_name)
    L = []
    for url in urls:
        # BeautifulSoup解析页面获取所有章节url
        soup = BeautifulSoup(get_html(url), 'lxml')
        all_td = soup.find_all('td', class_="L")
        # 定义一个存储章节标题的集合
        titlelist = []
        for a in all_td:
            # 这里有些小说会有作者写的一些通知，页面会和普通章节页不同，直接过滤报错
            try:
                titles = a.get_text()
                titlelist.append(titles)
            except Exception:
                pass
        L.append(titlelist)
    # print(L[0])
    return L


def get_author(search_name):
    urls = get_allbook_url(search_name)

    L = []
    for url in urls:
        # BeautifulSoup解析页面获取所有章节url
        soup = BeautifulSoup(get_html(url), 'lxml')
        author = soup.select('#a_main > div.bdsub > dl > dd > h3')[0].get_text()
        # a_main > div.bdsub > dl > dd:nth-child(4) > h3
        L.append(author)
    # print(L)
    return L

