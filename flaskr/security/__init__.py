from flask import Blueprint

bp = Blueprint('security', __name__)

from flaskr.security import script
