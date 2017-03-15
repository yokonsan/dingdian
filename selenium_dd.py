from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool
import requests
import time
import re
import os


class Dingdian(object):

    def __init__(self,search_name):
        self.search_name = search_name
        self.driver = webdriver.PhantomJS()

    def search_book(self,search_name):
        self.driver.get('http://www.23us.com/')
        assert "顶点" in self.driver.title
        print('正在搜索请稍等...')
        elem = self.driver.find_element_by_name('q')
        elem.send_keys(self.search_name)
        elem.send_keys(Keys.RETURN)
        self.driver.switch_to_window(self.driver.window_handles[1])
        info = self.driver.page_source
        self.get_search_url(info)

    def get_search_url(self,info):
        p = r'<a cpos="title" href="(.*?)" title="(.*?)"'
        result = re.findall(p, info)
        if result:
            for i in result:
                if self.search_name in i:
                    print(i[0])
                    self.get_all_url(i[0])
                else:
                    pass
        else:
            print('正则匹配出错了。')

    def get_all_url(self,url):
        list = []
        soup = BeautifulSoup(self.get_html(url), 'lxml')
        all_td = soup.find_all('td', class_="L")
        for a in all_td:
            try:
                html = a.find('a').get('href')
                htmls = url + html
                list.append(htmls)
            except:
                print('pass')
        print(list)
        self.download_book(list)

    def download_book(self,allurl):
        for each in set(allurl):
            soup = BeautifulSoup(self.get_html(each), 'lxml')
            #获取章节标题
            title = soup.title.text.split('-')[1]
            all_info = soup.find('dd', id="contents")
            #使用正则匹配章节内容
            p = r'<dd id="contents">(.*?)</dd>'
            #处理正则在匹配错误，都是作者牢骚的内容，不影响小说内容抓取，直接过滤
            try:
                info = re.findall(p, str(all_info), re.S)[0]
                #下载到txt文件
                with open(title + '.txt', 'w', encoding='gbk', errors='ignore') as f:
                    f.write(info.replace('<br/>', '\n'))
                    print('save sucessful: %s' % title)
            except:
                print('re faild: %s' % title)

    def get_html(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        html = requests.get(url,headers=headers).content

        return html


if __name__ == '__main__':
    start = time.time()
    os.mkdir('dingdian2')
    os.chdir('dingdian2')
    p = Pool(4)
    search_name = input('请输入要下载的小说名（注意错别字哦）：')
    test = Dingdian(search_name)
    p.apply_async(test.search_book(search_name))
    # test.search_book(search_name)
    print(int(time.time() - start))
