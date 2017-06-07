#!/usr/bin/env python
import os
from app import create_app
from flask_script import Manager, Shell

# gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
# gevent end


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
