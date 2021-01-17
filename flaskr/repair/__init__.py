from flask import Blueprint

bp = Blueprint('repair', __name__)

from flaskr.repair import books, collections, cities, copies, persons, publishers, rooms, series, shelves
