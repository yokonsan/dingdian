#!/usr/bin/env python
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from dingdian import db
from dingdian import create_app


app = create_app(os.getenv('CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    from flask_migrate import upgrade
    from dingdian.models import Search, Novel, Chapter, Article

    # 情况数据库
    searchs = Search.query.all()
    for s in searchs:
        db.session.delete(s)
    novels = Novel.query.all()
    for n in novels:
        db.session.delete(n)
    chapters = Chapter.query.all()
    for c in chapters:
        db.session.delete(c)
    articles = Article.query.all()
    for a in articles:
        db.session.delete(a)

    db.session.commit()

    # 更新数据库
    upgrade()

if __name__ == '__main__':
    manager.run()