import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PW = os.environ.get('DATABASE_PW')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASE_DB = os.environ.get('DATABASE_DB')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=DATABASE_USER,pw=DATABASE_PW,url=DATABASE_URL,db=DATABASE_DB)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Jacek_kuron'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
