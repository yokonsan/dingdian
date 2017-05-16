# Python爬虫 + Flask 实现小说网站
介绍
----
使用Python的selenium+PhantomJS实现爬虫，负责爬取顶点小说网的小说。使用Flask + Bootstrap简单部署。
小说搜索界面如下：<br>
<img src="https://github.com/Blackyukun/dingdian/blob/last/assets/img/peitu1.jpg" name="peitu1"><br>
章节列表：<br>
<img src="https://github.com/Blackyukun/dingdian/blob/last/assets/img/peitu2.jpg" name="peitu2"><br>
小说内容：<br>
<img src="https://github.com/Blackyukun/dingdian/blob/last/assets/img/peitu.jpg" name="peitu"><br>

使用
----
安装需要的包(windows)：<br>
```
(venv) $ pip install -r requirements.txt
```

运行程序(windows)：<br>
```
(venv) $ python manage.py runserver --host 0.0.0.0
```

爬虫
----
<ul>
	<li>
		利用selenium+PhantomJS+python抓取小说，需要环境查看<a href="https://github.com/Blackyukun/dingdian">这里</a>
	</li>
	<li>
		需要配置 mangodb 数据库，存储爬取内容，作为缓存，否则每次搜索抓取一次太慢
	</li>
</ul>

Flask实现
----
利用集成的Flask包 Flask_Bootstrap作为基模版渲染前端界面，利用 gevent 实现Flask异步非阻塞处理请求。
操作的时候舒服一些。
<br><br>
<h3>End!</h3>