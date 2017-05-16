from flask import session, render_template, redirect, url_for, flash, request
from ..spider.getcontens import get_allzj_title, get_author
from ..spider.booknums import contents_number, book_number
from ..spider.getpost import get_posts
from ..spider.download import download
from flask_cache import Cache
import os

from . import main
from .. import create_app

from .forms import SearchForm



app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# 我们使用了’simple’类型缓存，其内部实现是Werkzeug中的SimpleCache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@main.route('/',methods=['GET','POST'])
def index():
    cache.clear()
    form = SearchForm()
    if form.validate_on_submit():
        session['search_name'] = form.name.data
        return redirect(url_for('.search'))
    return render_template('index.html', form=form)

@main.route('/search')
def search():
    search_name = session.get('search_name')

    data = book_number(search_name)
    return render_template('search.html',data=data,search_name=search_name)

@main.route('/contents/<int:id>')
def contents(id):
    search_name = session.get('search_name')

    bookname = book_number(search_name)[id]
    session['bookname'] = bookname
    titles = get_allzj_title(search_name)[id]

    bookid = id
    data = contents_number(titles)

    author = get_author(search_name)[id]

    return render_template('contents.html',data=data,bookid=bookid,\
                           author=author,bookname=bookname)

@main.route('/post/<int:bookid>/<int:id>')
@cache.cached(timeout=300, key_prefix='view_%s', unless=None)
def post(bookid,id):

    search_name = session.get('search_name')

    title = get_allzj_title(search_name)[bookid][id]
    post = get_posts(search_name, bookid, id)

    return render_template('post.html', bookid=bookid, id=id,\
                           title=title,post=post,search_name=search_name)


@main.route('/download/<book>')
def download_book(book):

    search_name = session.get('search_name')
    # search_id = session.get('search_id')
    # bookname = session.get('bookname')

    titles = get_allzj_title(search_name)[0]
    data = contents_number(titles)

    flash('正在下载小说，请稍等。。。')
    download(book, data)
    flash('下载已经完成。')

    return render_template('download.html', book=book)
