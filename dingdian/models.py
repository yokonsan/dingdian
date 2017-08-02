from flask import url_for

from dingdian import db


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
    search_name = db.Column(db.String)
    page = db.Column(db.Integer)

    chapters = db.relationship('Chapter', backref='book', lazy='dynamic')

    def to_json(self):
        json_novel = {
            'url': url_for('api.get_result', search=self.search_name,_external=True),
            'book_name': self.book_name,
            'book_url': self.book_url,
            'book_img': self.book_img,
            'author': self.author,
            'style': self.style,
            'last_update': self.last_update,
            'profile': self.profile,
        }
        return json_novel

    def __repr__(self):
        return '<Novel %r>' % self.book_name


class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.String(64))
    chapter_url = db.Column(db.String, index=True)

    article = db.relationship('Article', backref='chapter', lazy='dynamic')
    book_id = db.Column(db.Integer, db.ForeignKey('novels.id'))

    def to_json(self):
        json_chapter = {
            'url': url_for('api.get_chapter', book_id=self.book_id, _external=True),
            'chapter_name': self.chapter,
            'chapter_url': self.chapter_url,
        }

        return json_chapter

    def __repr__(self):
        return '<Post %r>' % self.chapter

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))

    def to_json(self):
        json_article = {
            'url': url_for('api.get_content', chapter_id=self.chapter_id, _external=True),
            'content': self.content
        }

        return json_article

