# 导入需要的模块
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo
import re


client = pymongo.MongoClient('localhost', 27017)
dingdian = client['dingdian']
info_list = dingdian['info_list']


def search_name_html(search_name):
    driver = webdriver.PhantomJS()
    driver.get('http://www.23us.com/')
    # 断言
    assert "顶点" in driver.title
    # print('正在搜索请稍等...')
    # 找到输入框的name属性
    elem = driver.find_element_by_name('q')
    # 像输入框输入搜索的小说名
    elem.send_keys(search_name)
    # 相当于浏览器点击了回车
    elem.send_keys(Keys.RETURN)
    # 切换到新打开的页面
    driver.switch_to.window(driver.window_handles[1])
    # 获取新页面的源码
    info = driver.page_source
    return info


def get_search_url(search_name):
    info = search_name_html(search_name)
    p = r'<a cpos="title" href="(.*?)" title="(.*?)"'
    result = re.findall(p, info)
    if result:
        if info_list.find_one({search_name: result}):
            pass
        else:
            info_list.insert_one({search_name: result})
        return result
    else:
        pass



