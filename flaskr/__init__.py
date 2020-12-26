import os

from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_security.models import fsqla_v2 as fsqla
from elasticsearch import Elasticsearch

from config import Config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    fsqla.FsModels.set_db_info(db)
    mail = Mail(app)
    bootstrap.init_app(app)
    
    from flaskr.security.script import user_datastore
    app.security = Security(app, user_datastore)
    
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])\
            if app.config['ELASTICSEARCH_URL'] else None

    from flaskr.staff import bp as staff_bp
    app.register_blueprint(staff_bp)

    from flaskr.es_api import bp as es_bp
    app.register_blueprint(es_bp)

    from flaskr.accounts import bp as accounts_bp
    app.register_blueprint(accounts_bp)
    
    return app


from flaskr import models
