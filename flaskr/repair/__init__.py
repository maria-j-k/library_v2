from flask import Blueprint

bp = Blueprint('repair', __name__)

from flaskr.repair import publishers, series
