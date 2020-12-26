from flask import Blueprint

bp = Blueprint('accounts', __name__)

from flaskr.accounts import routes
