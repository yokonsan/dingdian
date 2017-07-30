from dingdian import db


class Search(db.Model):
    __tablename__ = 'searches'
    id = db.Column(db.Integer, primary_key=True)
    search_name = db.Column(db.String(64), index=True)

    novels = db.relationship('Novel', backref='search', lazy='joined')


class Novel(db.Model):
    __tablename__ = 'novels'
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(64), index=True)
    book_url = db.Column(db.String)
    book_img = db.Column(db.String)
    author = db.Column(db.String(64))
    style = db.Column(db.String(64), nullable=True)
    last_update = db.Column(db.String(64), nullable=True)
    profile = db.Column(db.Text, nullable=True)

    chapters = db.relationship('Chapter', backref='book', lazy='dynamic')
    search_name = db.Column(db.String, db.ForeignKey('searches.search_name'))


class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.String(64))
    chapter_url = db.Column(db.String, index=True)

    article = db.relationship('Article', backref='chapter', lazy='dynamic')
    book_id = db.Column(db.Integer, db.ForeignKey('novels.id'))


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))

