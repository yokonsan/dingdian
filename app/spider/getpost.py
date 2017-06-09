import re
from bs4 import BeautifulSoup
from .getcontens import get_html, get_allbook_url


def get_contents_url(search_name):
    urls = get_allbook_url(search_name)
    L = []
    for url in urls:
        # BeautifulSoup解析页面获取所有章节url
        soup = BeautifulSoup(get_html(url), 'lxml')
        all_td = soup.find_all('td', class_="L")
        # 定义一个存储章节url的集合
        urllist = []
        titlelist = []
        for a in all_td:
            # 这里有些小说会有作者写的一些通知，页面会和普通章节页不同，直接过滤报错
            try:
                html = a.find('a').get('href')
                htmls = url + html
                urllist.append(htmls)
            except Exception:
                pass
        L.append(urllist)
    return L


def get_posts(search_name, id, num):

    post_url = get_contents_url(search_name)[id][num]

    soup = BeautifulSoup(get_html(post_url), 'lxml')

    all_info = soup.find('dd', id="contents")
    # 使用正则匹配章节内容
    p = r'<dd id="contents">(.*?)</dd>'
    # 处理正则在匹配错误，都是作者牢骚的内容，不影响小说内容抓取，直接过滤
    try:
        post = re.findall(p, str(all_info), re.S)[0]
        Post = [i for i in post.split('<br/><br/>')]
        # Post.append(post)
        # Post.append(post)

    except Exception:
        pass
    # print(Post)
    return Post
