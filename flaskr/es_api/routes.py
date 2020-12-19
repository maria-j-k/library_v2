from csv import DictReader

from flask import flash, jsonify, redirect, render_template, request, url_for, g, current_app

from flaskr import db
from flaskr.es_api import bp
from flaskr.models import Book, Person



#@bp.route('/autocomplete_title')
#def autocomplete_title():
#    q = request.args.get('q')
#    books = Book.search_title(q)
#    return jsonify(matching_results=books)


@bp.route('/autocomplete_person') 
def autocomplete_person():
    q = request.args.get('q')
    persons = Person.search(q)
    return jsonify(matching_persons=persons)


@bp.route('/autocomplete_publisher') 
def autocomplete_publisher():
    q = request.args.get('q')
    publishers = Publisher.search(q)
    return jsonify(matching_publishers=publishers)

@bp.route('/es_fts/person')
def fts_title():
    q = request.args.get('q')
    fields = ['name']
    books = Book.es_search(q, fields)
