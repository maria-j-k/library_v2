from csv import DictReader

from flask import flash, jsonify, redirect, render_template, request, url_for, g, current_app

from flaskr import db
from flaskr.es_api import bp
from flaskr.es_api.queries import ac_person, ac_publisher, ac_serie, ac_city
from flaskr.models import Book, Person, Publisher, Serie, get_class_by_tablename



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
    return jsonify(matching_results=persons)

@bp.route('/autocomplete_city') 
def autocomplete_city():
    q = request.args.get('q')
    cities = ac_city(q)
#    publishers = Publisher.search(q)
    return jsonify(matching_results=cities)


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

@bp.route('/db_pub_place') # po modelu City
def find_pub_place():
    id = request.args.get('q')
    p = Publisher.query.get_or_404(id)
    return jsonify(Publisher.query.get_or_404(id).to_dict())

@bp.route('/es_fts/title')
def fts_title():
    q = request.args.get('q')
    fields = ['title']
    books = Book.es_search(q, fields)

#@bp.route('/toggle_incorrect')
#def toggle_incorrect():
#    q = request.args.get('q')
#    model = request.args.get('model')
#    tbl = get_class_by_tablename(model+'s')
#    obj = tbl.query.get(q)
#    print(obj)
#    print(q)
#    print(model)
#    return q
    

@bp.route('/toggle_incorrect', methods=['GET', 'POST'])
def toggle_incorrect():
    print(f'toggle {request.method}')
    tbl = get_class_by_tablename(request.args.get('m'))
    obj = tbl.query.get(request.args.get('id_'))
#    next_page = request.args.get('next')
    obj.toggle_incorrect()
    return jsonify({'id': obj.id, 'incorrect': obj.incorrect})
