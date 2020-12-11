from flask import Blueprint

bp = Blueprint('main', __name__)

from flaskr.staff import routes
