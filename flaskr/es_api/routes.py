from csv import DictReader

from flask import flash, jsonify, redirect, render_template, request, url_for, g, current_app

from flaskr import db
from flaskr.es_api import bp
from flaskr.es_api.queries import ac_person, ac_publisher, ac_serie
from flaskr.models import Book, Person, Publisher, Serie



#@bp.route('/autocomplete_title')
#def autocomplete_title():
#    '''trzeba będzie zmienić metodę search albo dopisać nową. 
#       Search szuka w _source "name", book ma "title".  '''
#    q = request.args.get('q')
#    books = Book.search_title(q)
#    return jsonify(matching_results=books)


@bp.route('/autocomplete_person') 
def autocomplete_person():
    q = request.args.get('q')
    persons = ac_person(q)
#    persons = Person.search(q)
    return jsonify(matching_persons=persons)


@bp.route('/autocomplete_publisher') 
def autocomplete_publisher():
    q = request.args.get('q')
    publishers = ac_publisher(q)
#    publishers = Publisher.search(q)
    return jsonify(matching_results=publishers)

@bp.route('/autocomplete_serie') 
def autocomplete_serie():
    q = request.args.get('q')
    publisher = request.args.get('publisher') 
    series = ac_serie(q, publisher)
    return jsonify(matching_results=series)

@bp.route('/db_pub_place')
def find_pub_place():
    id = request.args.get('q')
    p = Publisher.query.get_or_404(id)
    return jsonify(Publisher.query.get_or_404(id).to_dict())

@bp.route('/es_fts/title')
def fts_title():
    q = request.args.get('q')
    fields = ['title']
    books = Book.es_search(q, fields)
