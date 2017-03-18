# 导入需要的模块
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool
import requests
import time
import re
import os


# 爬虫类
class Dingdian(object):

    def __init__(self, search_name):
        """
        search_name是用户要输入的小说名，PhantomJS是一个没有界面的浏览器，
        selenuim也支持他的驱动，使用PhanJS是因为效率高。PhantomJS用来渲染解析JS，
        Selenium用来驱动并与Python的对接，Python 进行后期的处理工作。
        """
        self.search_name = search_name
        self.driver = webdriver.PhantomJS()

    def search_book(self, search_name):
        # 自动打开浏览器访问页面
        self.driver.get('http://www.23us.com/')
        # 断言
        assert "顶点" in self.driver.title
        print('正在搜索请稍等...')
        # 找到输入框的name属性
        elem = self.driver.find_element_by_name('q')
        # 像输入框输入搜索的小说名
        elem.send_keys(self.search_name)
        # 相当于浏览器点击了回车
        elem.send_keys(Keys.RETURN)
        # 切换到新打开的页面
        self.driver.switch_to.window(self.driver.window_handles[1])
        # 获取新页面的源码
        info = self.driver.page_source
        print('以获取信息...')
        return info

    def get_search_url(self, search_name):
        """
        使用正则从源码中匹配到搜索第一页的小说和链接，
        只获取第一页，如果有搜索的小说，那肯定会在第一页。
        """
        info = self.search_book(search_name)
        p = r'<a cpos="title" href="(.*?)" title="(.*?)"'
        result = re.findall(p, info)
        if result:
            for i in result:
                # 打印出搜索小说名对应的url
                if self.search_name in i:
                    print(i[0])
                    return i[0]
                else:
                    pass
        else:
            print('正则匹配出错了。')

    def get_all_url(self, search_name):
        # 定义一个存储章节url的集合
        list = []
        url = self.get_search_url(search_name)
        # BeautifulSoup解析页面获取所有章节url
        soup = BeautifulSoup(self.get_html(url), 'lxml')
        all_td = soup.find_all('td', class_="L")
        for a in all_td:
            # 这里有些小说会有作者写的一些通知，页面会和普通章节页不同，直接过滤报错
            try:
                html = a.find('a').get('href')
                htmls = url + html
                list.append(htmls)
            except Exception:
                pass
        print(list)
        return list
        # self.download_book(list)

    def download_book(self, search_name):
        for each in self.get_all_url(search_name):
            soup = BeautifulSoup(self.get_html(each), 'lxml')
            # 获取章节标题
            title = soup.title.text.split('-')[1]
            all_info = soup.find('dd', id="contents")
            # 使用正则匹配章节内容
            p = r'<dd id="contents">(.*?)</dd>'
            # 处理正则在匹配错误，都是作者牢骚的内容，不影响小说内容抓取，直接过滤
            try:
                info = re.findall(p, str(all_info), re.S)[0]
                # 下载到txt文件
                with open(title + '.txt', 'w', encoding='gbk', errors='ignore') as f:
                    f.write(info.replace('<br/>', '\n'))
                    print('save sucessful: %s' % title)
            except Exception:
                print('re faild: %s' % title)

    # 获取页面的response然后返回
    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        html = requests.get(url,headers=headers).content

        return html


if __name__ == '__main__':
    start = time.time()
    # 用户输入下载的小说名
    search_name = input('请输入要下载的小说名（注意错别字哦）：')
    # 转移工作路径
    os.mkdir(search_name)
    os.chdir(search_name)
    # 进程池
    p = Pool(4)
    
    # 实例化爬虫
    test = Dingdian(search_name)
    p.apply_async(test.download_book(search_name))
    # 打印下载的时间
    print(int(time.time() - start))
