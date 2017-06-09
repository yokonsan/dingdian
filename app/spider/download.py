from .getpost import get_posts
import os




def download(book, data):
    os.mkdir(book)
    os.chdir(book)
    for k, v in data.items():
        posts = get_posts(book, 0, k )
        # 下载到txt文件
        with open(v + '.txt', 'w', encoding='gbk', errors='ignore') as f:
            f.write(posts[0].replace('<br/>', '\n'))
            # print('save sucessful: %s' % v)

# download()
