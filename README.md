# dingdian

### 说明

由于顶点网站进行了一次更新，这次项目也进行一次大的更新。基本上是推翻前一次所有的实现方法。

### 爬虫实现

利用正则表达式加`requests`库，抓取顶点网的小说数据。

爬虫api调用：

- 搜索结果页：`DdSpider().get_index_result(search)`
- 小说章节页：`DdSpider().get_chapter(book_url)`
- 章节内容：`DdSpider().get_article(chapter_url)`

爬虫封装在DdSpider类中，如果网站再次更新，只要改动爬虫类就可以了。

### FLask

每次启动爬虫由`SQLAlchemy`数据库保存数据，加快再次访问速度。

过段时间可能有还在连载的小说会有更新那么需要清空数据库，再启动。

### 查看详情

知乎[传送门](https://zhuanlan.zhihu.com/p/28216335)

