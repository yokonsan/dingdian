from flask import flash, render_template, url_for, redirect
from flask.blueprints import Blueprint

from dingdian import db
from .forms import SearchForm
from ..spider.spider import DdSpider
from ..models import Search, Novel, Chapter, Article


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search_name.data
        data = Search(search_name=search)
        db.session.add(data)
        flash('搜索成功。')
        return redirect(url_for('main.result', search=search))
    return render_template('index.html', form=form)

@main.route('/results/<search>')
def result(search):
    # 查找数据库中search键相等的结果，如果有则不需要调用爬虫，直接返回
    books = Novel.query.filter_by(search_name=search).all()
    if books:
        return render_template('result.html', books=books)
    spider = DdSpider()
    for data in spider.get_index_result(search):
        novel = Novel(book_name=data['title'],
                      book_url=data['url'],
                      book_img=data['image'],
                      author=data['author'],
                      style=data['style'],
                      profile=data['profile'],
                      last_update=data['time'],
                      search_name=search)
        db.session.add(novel)
    books = Novel.query.filter_by(search_name=search).all()
    return render_template('result.html', books=books)

@main.route('/chapter/<int:book_id>')
def chapter(book_id):
    chapters = Chapter.query.filter_by(book_id=book_id).all()
    if chapters:
        return render_template('chapter.html', chapters=chapters)
    spider = DdSpider()

    book = Novel.query.filter_by(id=book_id).first()
    for data in spider.get_chapter(book.book_url):
        chapter = Chapter(chapter=data['chapter'],
                           chapter_url=data['url'],
                           book_id=book_id)
        db.session.add(chapter)
    chapters = Chapter.query.filter_by(book_id=book_id).all()
    return render_template('chapter.html', chapters=chapters)

@main.route('/content/<int:chapter_id>')
def content(chapter_id):
    # 这里有出bug，记得改
    article = Article.query.filter_by(chapter_id=chapter_id)
    if article:
        return render_template('article.html', article=article)
    spider = DdSpider()

    chapter = Chapter.query.filter_by(id=chapter_id).first()
    article2 = Article(content=spider.get_article(chapter.chapter_url),
                      chapter_id=chapter_id)
    db.session.add(article2)
    return render_template('article.html', article=article2)
