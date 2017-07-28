import requests


url = 'http://zhannei.baidu.com/cse/search?q=%E8%AF%9B%E4%BB%99&p=0&s=1682272515249779940'
html = requests.get(url)
html.encoding = 'utf-8'
print(html.text)