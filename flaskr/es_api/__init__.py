from flask import Blueprint

bp = Blueprint('es_api', __name__)

from flaskr.es_api import routes
