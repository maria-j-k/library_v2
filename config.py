import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PW = os.environ.get('DATABASE_PW')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASE_DB = os.environ.get('DATABASE_DB')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Jacek_kuron'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=os.environ.get('MAIL_PORT', '587')
    MAIL_USE_TLS=1
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX='Biblioteka WLH'
    MAIL_SENDER='Biblioteka WLH <wlh.biblioteka@gmail.com>'
    BOOTSTRAP_BOOTSWATCH_THEME = 'sandstone'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=Config.DATABASE_USER,pw=Config.DATABASE_PW,url=Config.DATABASE_URL,db=Config.DATABASE_DB)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    pass


config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,

        'default': DevelopmentConfig
        }





