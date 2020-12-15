from flask import Blueprint

bp = Blueprint('staff', __name__)

from flaskr.staff import routes
