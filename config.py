import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RECORDS_PER_PAGE = 10

    MAIL_SERVER = 'localhost'

    MAIL_PORT = 25
    MAIL_USE_SSL = False
    # MAIL_USERNAME = 'admin@localhost'
    # MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = 'admin@localhost'
    ADMINS = ['admin@localhost']