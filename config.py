import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PW = os.environ.get('DATABASE_PW')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASE_DB = os.environ.get('DATABASE_DB')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=DATABASE_USER,pw=DATABASE_PW,url=DATABASE_URL,db=DATABASE_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Jacek_kuron'
    SECURITY_PASSWORD_HASH = os.environ.get('SECURITY_PASSWORD_HASH') 
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_REGISTERABLE = True
    MAIL_SERVER=os.environ.get('MAIL_SERVER')
    MAIL_PORT=os.environ.get('MAIL_PORT')
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')



