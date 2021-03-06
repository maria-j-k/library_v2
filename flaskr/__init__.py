import os
from elasticsearch import Elasticsearch

from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'users.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])\
            if app.config['ELASTICSEARCH_URL'] else None

    from flaskr.staff import bp as staff_bp
    app.register_blueprint(staff_bp)

    from flaskr.repair import bp as repair_bp
    app.register_blueprint(repair_bp, url_prefix='/repair')

    from flaskr.users import bp as users_bp
    app.register_blueprint(users_bp)

    from flaskr.es_api import bp as es_bp
    app.register_blueprint(es_bp)

    return app


from flaskr import models
