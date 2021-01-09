from flask import Blueprint

bp = Blueprint('repair', __name__)

from flaskr.repair import books, collections, cities, copies, locations, persons, publishers, series
