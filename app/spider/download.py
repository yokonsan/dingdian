# from .getcontens import get_allzj_title
from .getpost import get_posts
# from .booknums import contents_number
import os




def download(book, data):
    # titles = get_allzj_title('诛仙')[0]
    # data = contents_number(titles)
    os.mkdir(book)
    os.chdir(book)
    for k, v in data.items():
        posts = get_posts(book, 0, k )
        # 下载到txt文件
        with open(v + '.txt', 'w', encoding='gbk', errors='ignore') as f:
            f.write(posts[0].replace('<br/>', '\n'))
            # print('save sucessful: %s' % v)

# download()