#!/usr/bin/env python
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from dingdian import db
from dingdian import create_app


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()