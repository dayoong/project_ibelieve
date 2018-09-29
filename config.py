# -*- coding: utf8 -*-
import os, pusher
from datetime import date

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['cdy0266@gmail.com']

# Whoosh does not work on Heroku
WHOOSH_ENABLED = os.environ.get('HEROKU') is None

# pusher
p = pusher.Pusher(
    app_id='153732',
    key='444551662290f746b4db',
    secret='efb5648c6338fda0321b'
)

# pagination
POSTS_PER_PAGE = 1
prev_num = 1
next_num = 1
sDate = date.today()

# var
select_child = 0
